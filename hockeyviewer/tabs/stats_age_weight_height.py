from dash import html, dcc, dash_table, Input, Output, State

import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text


from hockeyviewer.nhlscraper import teamcolors
from hockeyviewer.tasks import df_people
from app import app, engine

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}

def compare_stats_attr():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(["Controls"], className="card-header"),
                            html.Div(
                                [
                                    html.Div("X-Axis", className="control--label"),
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id="drop-stats-ahw-xaxis",
                                                options=[
                                                    {"label": "Age", "value": "currentAge"},
                                                    {"label": "BMI", "value": "bmi"},
                                                    {"label": "Height", "value": "height_calc"},
                                                    {"label": "Weight", "value": "weight"}
                                                ],
                                                value="bmi",
                                                clearable=False,
                                                style={"width": "100%"}
                                            )
                                        ],
                                        className="control--item",
                                    )
                                ],
                                className="control control--vertical label--top label--text--left",
                                style={"width": "calc(100% - 0px)"}
                            ),
                            html.Div(
                                [
                                    html.Div("Y-Axis", className="control--label"),
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id="drop-stats-ahw-yaxis",
                                                options=[
                                                    {"label": "PPG", "value": "ppg"},
                                                ],
                                                value="ppg",
                                                clearable=False,
                                                style={"width": "100%"}
                                            )
                                        ],
                                        className="control--item",
                                    )
                                ],
                                className="control control--vertical label--top label--text--left",
                                style={"width": "calc(100% - 0px)"}
                            ),
                        ],
                        className="card--content"
                    )
                ],
                className="block card",
                style={"width": "calc(10% - 0px)"}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([" Plot for Average by Team"], className="card-header"),
                            dbc.Spinner([dcc.Graph(id="plot-stats-ahw")], color="primary", type="grow")
                        ],
                        className="card--content"
                    )
                ],
                className="block card",
                style={"width": "calc(80% - 0px)"}
            ),
        ],
        className="row"
    )

layout = html.Div(
    [
        compare_stats_attr(),
    ]
)

@app.callback(
    Output("plot-stats-ahw", "figure"),
    [Input("drop-stats-ahw-xaxis", "value"),
    Input("drop-stats-ahw-yaxis", "value")]
)

def build_compareall_stats(xaxis, yaxis):
    query_ppl_stats = 'SELECT * FROM playersTenStats'
    df_ppl_stats = pd.read_sql_query(sql=text(query_ppl_stats), con=engine.connect())
    df = df_ppl_stats.merge(df_people, left_on='person.id', right_on='id')
    # add bmi col
    df['bmi'] = (df['weight'].astype(int) / df['height_calc'].astype(int) / df['height_calc'].astype(int))*703
    # add ppg col
    df['ppg'] = df['stat.points']/df['stat.games']
    # keep 20 games or more for season
    df_20 = df[df['stat.games'] >= 20]

    # create bin based on selection
    df_20['bins'] = pd.qcut(df_20[xaxis], 4)
    df_20 = df_20.sort_values(by=['bins'])
    df_20['bins'] = df_20['bins'].astype(str)
    plot = px.box(df_20, x='bins', y=yaxis, color='primaryPosition.name')

    plot.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=20, t=20, b=20),
        showlegend=True
    )
    plot.update_xaxes(
        title="<b>{}".format(xaxis),
        row=1,
        col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='Gray'
    )
    plot.update_yaxes(
        title="<b>{}".format(yaxis),
        row=1,
        col=1,
        showgrid=True,
        gridwidth=1,
        gridcolor='Gray'
    )
    return plot
