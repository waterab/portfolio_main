# Build requests modules
import pandas as pd
import requests
import json
import asyncio
import aiohttp

teamcolors = {
    'Anaheim Ducks' : '#F47A38',
    'Arizona Coyotes' : '#862633',
    'Boston Bruins' : '#FFB81C',
    'Buffalo Sabres' : '#002654',
    'Calgary Flames' : '#C8102E',
    'Carolina Hurricanes' : '#CC0000',
    'Chicago Blackhawks' : '#CF0A2C',
    'Colorado Avalanche' : '#6F263D',
    'Columbus Blue Jackets' : '#002654',
    'Dallas Stars' : '#006847',
    'Detroit Red Wings' : '#CE1126',
    'Edmonton Oilers' : '#041E42',
    'Florida Panthers' : '#041E42',
    'Los Angeles Kings' : '#111111',
    'Minnesota Wild' : '#154734',
    'Montréal Canadiens' : '#AF1E2D',
    'Nashville Predators' : '#FFB81C',
    'New Jersey Devils' : '#CE1126',
    'New York Islanders' : '#F47D30',
    'New York Rangers' : '#0038A8',
    'Ottawa Senators' : '#C52032',
    'Philadelphia Flyers'  : '#F74902',
    'Pittsburgh Penguins'  : '#FCB514',
    'San Jose Sharks'  : '#006D75',
    "Seattle Kraken": "#99D9D9",
    'St. Louis Blues'  : '#002F87',
    'Tampa Bay Lightning' : '#002868',
    'Toronto Maple Leafs' : '#00205B',
    'Vancouver Canucks' : '#00205B',
    'Vegas Golden Knights' : '#B4975A',
    'Washington Capitals' : '#C8102E',
    'Winnipeg Jets' : '#041E42',
}


class nhlstats():

    def __init__(self):
        self.url = "https://statsapi.web.nhl.com/api/v1/"

    def player(self, player_id):
        url = self.url + "people" + "/{}".format(self.player_id)
        r = requests.get(url)
        js = r.json()
        df = pd.json_normalize(js)
        return df

    def playerSeasonStats(self, player_id, season):
        url = self.url + "people/{}/stats?stats=statsSingleSeason&season={}".format(player_id, season)
        r = requests.get(url)
        js = r.json()
        df = pd.json_normalize(js["stats"], record_path=["splits"])
        return df

    def seasons(self):
        url = self.url + "seasons"
        r = requests.get(url)
        js = r.json()
        df = pd.json_normalize(js["seasons"])
        return df

    def standings(self):
        url = self.url + "standings"
        js = requests.get(url).json()
        df = pd.json_normalize(js["records"], record_path=["teamRecords"])
        return df

    # IF YOU CAN COMBINE TEAMS INTO ONE FUNCTION WITH SUBFUNCTIONS
    def teamsList(self):
        url = self.url + "teams"
        js = requests.get(url).json()
        df = pd.json_normalize(js["teams"])
        return df

    def teamStats(self, team_id=None, season=None):

        if team_id is not None:
            url = self.url + "teams" + "/{}".format(team_id)
        else:
            url = self.url + "teams"

        try:
            if season is not None:
                r = requests.get(url + "?expand=team.stats" + "&season={}".format(season))
            else:
                #current season
                r = requests.get(url + "?expand=team.stats")
            js = r.json()
            df = pd.json_normalize(data=js["teams"], record_path=["teamStats", "splits"])
            return df
        except:
            df = pd.DataFrame()
            return df

    def teamRoster(self, team_id=None, season=None):

        if team_id is not None:
            url = self.url + "teams" + "/{}".format(team_id)
        else:
            url = self.url + "teams"

        if season is not None:
            r = requests.get(url + "?expand=team.roster" + "&season={}".format(season))
        else:
            #current season
            r = requests.get(url + "?expand=team.roster")
        js = r.json()
        df = pd.json_normalize(data=js["teams"], record_path=["roster", "roster"], meta=["id", "name"])
        return df

    def teamLogo(team_id):
        if team_id is None:
            return 'Error: team id required'
        else:
            url = 'https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/' + str(team_id)  + '.svg'
            return url
