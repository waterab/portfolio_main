from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from hockeyviewer.nhlscraper import nhlstats, teamcolors
from app import app

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}

df_teams = nhlstats().teamsList ()
df_records = nhlstats().standings()
df_team_records = df_teams.merge(df_records, left_on="name", right_on="team.name")
# division
# conference
# league
def rank_place(cat, df):
    if cat != "league":
        df_all = pd.DataFrame()
        for x in df["{}.name".format(cat)].unique():
            df_x = df[df["{}.name".format(cat)] ==  x]
            df_all = df_all.append(df_x)
        #df_all["leagueRecord.wins"] = df_all["leagueRecord.wins"].astype(int)
        df_all = df_all.sort_values(by=["points"], ascending=False)
        plot = px.bar(df_all, x="team.name", y="leagueRecord.wins", text="{}Rank".format(cat))
        return df_all
    else:
        df_plot =  df.sort_values(by=["points"], ascending=False)
        plot = px.bar(df_plot, x="team.name", y="leagueRecord.wins", text="leagueRank")
        return df_plot

def standings_div(cat, df):
    div_standings = rank_place(cat, df)
    div_all = []
    for x_type in div_standings["{}.name".format(cat)].unique():
        df_div = div_standings[div_standings["{}.name".format(cat)] == x_type]
        #df_table = df_div[["team.name", "leagueRecord.wins", "{}Rank".format(cat)]]
        def f(row):
            logo = app.get_asset_url('logos/' + str(row['team.id']) + '.svg')
            return '![{0}]({0}#thumbnail)'.format(logo)
        df_div.insert(loc=0, column='', value=df_div.apply(f, axis=1))
        df_table = df_div[["", "team.name", "points", "leagueRecord.wins", "regulationWins", "goalsScored", "goalsAgainst"]]
        table = dash_table.DataTable(
            id="table-standings",
            columns=[{'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df_table.columns],
            data=df_table.to_dict('records'),
            page_size=10,
            sort_action="native",
            style_header={
                'fontWeight': 'bold',
                'font-family': '"Open Sans", sans-serif',
                'textAlign': 'center',
                'font-size': '10px',
                'vertical-align': 'middle',
                #'background-color': 'black',
                #'color': 'white'
            },
            style_cell={
                'textAlign': 'center',
                'fontWeight': 'bold',
                'font-family': '"Open Sans", sans-serif',
                'border': '1px solid #F7F7F7',
                'border-bottom': '1px solid black',
                'font-size': '12px',
                'backgroundColor': '#F7F7F7',
                'maxHeight': '40px',
                'minWidth': '0px', 'maxWidth': '96px',

            },
            style_cell_conditional=[
                {'if': {'column_id': ''},
                 'minWidth': '40px', 'width': '50px', 'maxWidth': '40px',
                 'textAlign': 'center',},
            ],
            style_table={
                'padding': '0px',
            },
            style_as_list_view=True,
        )
        plot = px.bar(df_div, y="team.name", x="leagueRecord.wins", custom_data=["id"], text="{}Rank".format(cat), color="team.name", color_discrete_map=teamcolors, orientation="h")
        plot.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=20, t=20, b=20),
        )
        plot.update_yaxes(showticklabels=False, title="")
        plot.update_xaxes(title="<b>Total Wins</b>")
        # plot_team.update_xaxes(title="<b>Team", type="category")
        # plot_team.update_yaxes(
        #     title="<b>Current {}".format(map_stats[col]),
        #     showgrid=True,
        #     gridwidth=1,
        #     gridcolor='Gray'
        # )
        # # Add logo
        for x in plot['data']:
            if x['y'] is not None:
                team = x['legendgroup']
                team_x = x['y']
                team_y = x['x']
                team_id = x["customdata"][0][0]
                # find logo url based on team name
                logo = app.get_asset_url('logos/' + str(team_id) + '.svg')
                plot.add_layout_image(
                    dict(
                        source=logo,
                        y=np.array(team_x[0]),
                        x=np.array(team_y[0]+5),
                    ))
        plot.update_layout_images(dict(
                xref="x",
                yref="y",
                sizex=10,
                sizey=10,
                xanchor='center',
                yanchor='middle'
        ))
        # add bar for total games = 82
        plot.add_trace(go.Bar(y=df_div["team.name"], x=[82]*len(df_div["team.name"]), name="Total Games", opacity=0.2, marker=dict(color="gray"), orientation="h"))
        plot.update_layout(barmode="overlay")
        div = html.Div(
            [
                html.Div(
                    [
                        html.Div(["{}".format(x_type)], className="card-header", style={"text-align": "center"}),
                        dcc.Graph(figure=plot),
                        table
                    ],
                    className="card--content"
                )
            ],
            className="block card",
            style={"flex": "1", "flex-shrink": "0", "width": "calc(50% - 0px)"}
        )
        div_all.append(div)
    return html.Div(div_all, style={"display": "flex", "flex-wrap": "wrap"})


layout = html.Div(
    [
        html.Div(
            [
                dcc.Tabs(id="tabs-standings", value='division',
                    children=[
                        dcc.Tab(label='League', value='league', selected_style=tab_selected_style),
                        dcc.Tab(label='Conference', value='conference', selected_style=tab_selected_style),
                        dcc.Tab(label='Division', value='division', selected_style=tab_selected_style),
                        #dcc.Tab(label='Player Birth', value='tab-birth', selected_style=tab_selected_style),
                        #dcc.Tab(label='Player Nationality', value='tab-nationality', selected_style=tab_selected_style),
                        #dcc.Tab(label='Team Shots', value='tab-nationality', selected_style=tab_selected_style)
                    ],
                ),
            ],
            className="layout-tabs"
        ),
        html.Div(id="page-standings")
    ],
    className="ddk-container"
)

@app.callback(
    Output("page-standings", "children"),
    Input("tabs-standings", "value")
)

def update_standingspage(tab):
    return standings_div(tab, df_team_records),
