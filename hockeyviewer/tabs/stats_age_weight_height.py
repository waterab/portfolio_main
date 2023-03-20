from dash import html, dcc, dash_table

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from hockeyviewer.nhlscraper import teamcolors
from hockeyviewer.tasks import df_people
from app import app

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
                                                    {"label": "Age", "value": "Age"},
                                                    {"label": "Height", "value": "Height"},
                                                    {"label": "Weight", "value": "Weight"}
                                                ],
                                                value="Height",
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
                                                    {"label": "Age", "value": "Age"},
                                                    {"label": "Height", "value": "Height"},
                                                    {"label": "Weight", "value": "Weight"}
                                                ],
                                                value="Weight",
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
    [Output("plot-ahw", "figure"),,
    [Input("drop-ahw-xaxis", "value"),
    Input("drop-ahw-yaxis", "value")]
)

def build_compareall_stats(xaxis, yaxis):
    plot.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=20, t=20, b=20),
        showlegend=False
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
