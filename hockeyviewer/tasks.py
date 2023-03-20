import datetime
import time
import json
import numpy as np
import os
import pandas as pd
from pandas.io.json import json_normalize
import plotly
import redis
from multiprocessing.pool import ThreadPool
import asyncio
import aiohttp
import time
import urllib.request
from sqlalchemy import create_engine, text

from hockeyviewer.nhlscraper import nhlstats
from app import engine

def store_seasonal():
    # Team Names
    teamslist = nhlstats().teamsList().sort_values(by=['name'])
    team_idname = teamslist[['id', 'name']]
    # Team logos - stores images in assets folder
    for id in team_idname['id']:
        logo_url = nhlstats.teamLogo(team_id=id)
        urllib.request.urlretrieve(logo_url, "assets/logos/" + (str(id) + ".svg"))
    return teamslist

def collect_playerdetails_basic():
    # Latest season player info
    async def get(player_id):
        url = "https://statsapi.web.nhl.com/api/v1/people/{}".format(str(player_id))
        headers = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
             'Cache-Control': 'no-cache',
             'Pragma': 'no-cache'
        }
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url=url) as response:
                    response = await session.request(method='GET', url=url)
                    response.raise_for_status()
                    response_json = await response.json()
                    df = pd.json_normalize(data=response_json["people"])
                    #print("Successfully got url {} with response of length {}.".format(url, len(response)))
                    return df
        except Exception as e:
            print("Unable to get url {} due to {}.".format(url, e))

    async def main(urls, amount):
        ret = await asyncio.gather(*[get(url) for url in urls])
        print("Finalized all. ret is a list of len {} outputs.".format(len(ret)))
        return ret
    urls = nhlstats().teamRoster()["person.id"].tolist()
    amount = len(urls)
    response = asyncio.get_event_loop().run_until_complete(main(urls, amount))
    #response = asyncio.run(main(urls, amount))
    df_people = pd.concat(response)
    # Store in local database
    df_people.to_sql("players", con=engine, if_exists="replace")

def update_players():
    print("----> update_players")
    # List of current teamids
    teamslist = nhlstats().teamsList().sort_values(by=['name'])
    teamids = teamslist['id'].tolist()
    # View roster for each team
    df_players = pd.DataFrame()
    for team_id in teamids:
       df_roster = nhlstats().teamRoster(str(team_id))
       df_players = df_players.append(df_roster)
    # Threader for building list of players
    def build_playerlist(team_id):
        df_players = pd.DataFrame()
        df_roster = nhlstats().teamRoster(str(team_id))
        df_players = df_players.append(df_roster)
        return df_players
    # Use threader
    def run_downloader_playerlist(process:int, teamids:list):
        df_players = pd.DataFrame()
        results = ThreadPool(process).imap_unordered(build_playerlist, teamids)
        for r in results:
            df_players = df_players.append(r)
        return df_players
    try:
        num_process = int(sys.argv[2])
    except:
        num_process = 10
    df_players = run_downloader_playerlist(num_process, teamids)
    df_players.to_sql('players', con=engine, if_exists='replace')
    # # Save the dataframe in redis so that the Dash app, running on a separate
    # # process, can read it
    # redis_instance.hset(
    #     REDIS_HASH_NAME,
    #     REDIS_KEYS["CURRENT_PLAYERS"],
    #     json.dumps(
    #         df_players.to_dict(),
    #         # This JSON Encoder will handle things like numpy arrays
    #         # and datetimes
    #         cls=plotly.utils.PlotlyJSONEncoder,
    #     ),
    # )

# store_seasonal()
collect_playerdetails_basic()
# update_players()

# All seasons
seasons = nhlstats().seasons()["seasonId"].to_list()
latest_season = seasons[-1] # latest season from list

query_people = 'SELECT * FROM players'
df_people = pd.read_sql_query(sql=text(query_people), con=engine.connect())
df_people["height_feet"] = df_people["height"].str.split("'").str[0].astype(int)
df_people["height_in"] = df_people["height"].str.split(" ").str[-1].str.replace("\"", "").astype(int)
df_people["height_calc"] = df_people["height_feet"]*12 + df_people["height_in"]
