from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from hockeyviewer.nhlscraper import nhlstats, teamcolors
from hockeyviewer.tasks import df_people
from app import app

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}

def build_detail_row(col):
    # standings data
    df_teams = nhlstats().teamsList()
    df_records = nhlstats().standings()
    df_team_records = df_teams.merge(df_records, left_on="name", right_on="team.name")
    print(df_team_records)
    print(df_team_records.columns)

    map_stats = {
        "currentAge": "Age",
        "height_calc": "Height",
        "weight": "Weight"
    }
    # isolate points from teams records and add to player attributes
    df_points = df_team_records[['id', 'name', 'leagueRecord.wins']]
    # use mean for player attrib due to points being a team effort
    df_attr_mean = df_people.groupby(['currentTeam.id'], as_index=False)[['currentAge', 'height_calc', 'weight']].mean().round(1)
    df_pnts_attrmean = df_points.merge(df_attr_mean, left_on='id', right_on='currentTeam.id').drop(columns=['currentTeam.id'])

    div_pnts_attrmean = []
    for attr in ['currentAge', 'height_calc', 'weight']:
        print(attr)
        plot = px.scatter(df_pnts_attrmean, x=attr, y='leagueRecord.wins', color='name')
        div_pnts_attrmean.append(html.Div([dcc.Graph(id="plot-{}".format(attr), figure=plot, className="dash-graph ddk-graph")]))
        print(div_pnts_attrmean)
    return html.Div(div_pnts_attrmean)

    # Plots
    # plot = px.histogram(df, x=col, marginal="box", color_discrete_sequence=['#242a44'])
    # plot.update_layout(
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     margin=dict(l=0, r=20, t=20, b=20),
    # )
    # plot.update_xaxes(
    #     title="<b>Current {}".format(map_stats[col]),
    #     row=1,
    #     col=1,
    # )
    # plot.update_yaxes(
    #     title="<b>Total Players",
    #     row=1,
    #     col=1,
    #     showgrid=True,
    #     gridwidth=1,
    #     gridcolor='Gray'
    # )
    # #df_people_mean_col = df_people_mean_col.sort_values(by=[col], ascending=False)
    # plot_team = px.box(df_people_mean_col, x="currentTeam.name", y=col, color="currentTeam.name", color_discrete_map=teamcolors, custom_data=["currentTeam.id"])
    # plot_team.update_layout(
    #     showlegend=False,
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     margin=dict(l=0, r=20, t=20, b=20),
    # )
    # plot_team.update_xaxes(title="<b>Team", type="category")
    # plot_team.update_yaxes(
    #     title="<b>Current {}".format(map_stats[col]),
    #     showgrid=True,
    #     gridwidth=1,
    #     gridcolor='Gray'
    # )
    # # Add logo
    # for x in plot_team['data']:
    #     if x['x'] is not None:
    #         team = x['legendgroup']
    #         team_x = x['x']
    #         team_y = x['y']
    #         team_id = x["customdata"][0][0]
    #         # find logo url based on team name
    #         logo = app.get_asset_url('logos/' + str(team_id) + '.svg')
    #         plot_team.add_layout_image(
    #             dict(
    #                 source=logo,
    #                 x=np.array(team_x[0]),
    #                 y=np.array(map_teammean[team_id]),
    #             ))
    # plot_team.update_layout_images(dict(
    #         xref="x",
    #         yref="y",
    #         sizex=(df[col].max()-df[col].min())/10,
    #         sizey=(df[col].max()-df[col].min())/10,
    #         xanchor='center',
    #         yanchor='middle'
    # ))
    # # Table averages
    # df_mean_table = df_people.groupby(["currentTeam.id", "currentTeam.name"])[col].mean().round(0).reset_index()
    # df_mean_table = df_mean_table.sort_values(by=[col], ascending=False)
    # df_mean_table.columns = ["id", "Team", col]
    # def f(row):
    #     logo = app.get_asset_url('logos/' + str(row['id']) + '.svg')
    #     return '![{0}]({0}#thumbnail)'.format(logo)
    # df_mean_table.insert(loc=0, column='', value=df_mean_table.apply(f, axis=1))
    # df_mean_table = df_mean_table[["", "Team", col]]
    # table = dash_table.DataTable(
    #     columns=[{'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df_mean_table.columns],
    #     data=df_mean_table.to_dict('records'),
    #     page_size=7,
    #     sort_action="native",
    #     style_header={
    #         'fontWeight': 'bold',
    #         'font-family': '"Open Sans", sans-serif',
    #         'textAlign': 'center',
    #         'font-size': '10px',
    #         'vertical-align': 'middle',
    #         #'background-color': 'black',
    #         #'color': 'white'
    #     },
    #     style_cell={
    #         'textAlign': 'center',
    #         'fontWeight': 'bold',
    #         'font-family': '"Open Sans", sans-serif',
    #         'border': '1px solid #F7F7F7',
    #         'border-bottom': '1px solid black',
    #         'font-size': '12px',
    #         'backgroundColor': '#F7F7F7',
    #         'maxHeight': '40px',
    #         'minWidth': '0px', 'maxWidth': '96px',
    #
    #     },
    #     style_cell_conditional=[
    #         {'if': {'column_id': ''},
    #          'minWidth': '40px', 'width': '50px', 'maxWidth': '40px',
    #          'textAlign': 'center',},
    #     ],
    #     style_table={
    #         'padding': '0px',
    #     },
    #     style_as_list_view=True,
    # )
    # return html.Div(
    #     [
    #         html.Div(
    #             [
    #                 html.Div(
    #                     [
    #                         html.Div(["{} of All Current Players".format(map_stats[col])], className="card-header"),
    #                         dcc.Graph(id="plot-{}".format(map_stats[col]), figure=plot
    #                         ),
    #                     ],
    #                     className="card--content"
    #                 )
    #             ],
    #             className="block card",
    #             style={"width": "calc(30% - 0px)"}
    #         ),
    #         html.Div(
    #             [
    #                 html.Div(
    #                     [
    #                         html.Div(
    #                             [
    #                                 "{} of Current Players by Team".format(map_stats[col]),
    #                             ],
    #                             className="card-header",
    #                             style={"justify-content": "space-between"}
    #                         ),
    #                         dcc.Graph(id="plot-age-team", figure=plot_team, className="dash-graph ddk-graph"),
    #                     ],
    #                     className="card--content"
    #                 )
    #             ],
    #             className="block card",
    #             style={"width": "calc(45% - 0px)"}
    #         ),
    #         html.Div(
    #             [
    #                 html.Div(
    #                     [
    #                         html.Div(
    #                             [
    #                                 "Average {} of Current Players by Team".format(map_stats[col]),
    #                             ],
    #                             className="card-header",
    #                             style={"justify-content": "space-between"}
    #                         ),
    #                         table
    #                     ],
    #                     className="card--content"
    #                 )
    #             ],
    #             className="block card",
    #             style={"width": "calc(20% - 0px)"}
    #         )
    #     ],
    #     className="row"
    # )


layout = html.Div(
    [
        build_detail_row("currentAge"),
    ]
)

# @app.callback(
#     Output("drop-ahw-zaxis-div", "style"),
#     [Input("toggle-ahw-3dview", "value")]
# )
#
# def toggle_zaxis(toggle_3d):
#     if 1 not in toggle_3d:
#         return {"display": "none"}
#     else:
#         return {"width": "100%"}
#
# @app.callback(
#     [Output("plot-ahw", "figure"),
#     Output("table-ahw", "data"),
#     Output("table-ahw", "columns")],
#     [Input("toggle-ahw-3dview", "value"),
#     Input("drop-ahw-xaxis", "value"),
#     Input("drop-ahw-yaxis", "value"),
#     Input("drop-ahw-zaxis", "value")]
# )
#
# def build_compareall(toggle_3d, xaxis, yaxis, zaxis):
#     df = df_people.groupby(['currentTeam.id', 'currentTeam.name']).agg(
#         Age=('currentAge', 'mean'),
#         Height=('height_calc', 'mean'),
#         Weight=('weight', 'mean')
#     ).reset_index()
#     df.columns = ["id", "Team", "Age", "Height", "Weight"]
#     df["Age"] = df["Age"].round(1)
#     df["Height"] = df["Height"].round(1)
#     df["Weight"] = df["Weight"].round(1)
#     if 1 not in toggle_3d:
#         plot = px.scatter(df, x=xaxis, y=yaxis, color="Team", color_discrete_map=teamcolors, custom_data=["id"])
#         plot.update_layout(
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)',
#             margin=dict(l=0, r=20, t=20, b=20),
#             showlegend=False
#         )
#         plot.update_xaxes(
#             title="<b>{}".format(xaxis),
#             row=1,
#             col=1,
#             showgrid=True,
#             gridwidth=1,
#             gridcolor='Gray'
#         )
#         plot.update_yaxes(
#             title="<b>{}".format(yaxis),
#             row=1,
#             col=1,
#             showgrid=True,
#             gridwidth=1,
#             gridcolor='Gray'
#         )
#         # Add logo
#         for x in plot['data']:
#             if x['x'] is not None:
#                 team = x['legendgroup']
#                 team_x = x['x']
#                 team_y = x['y']
#                 team_id = x["customdata"][0][0]
#                 # find logo url based on team name
#                 logo = app.get_asset_url('logos/' + str(team_id) + '.svg')
#                 plot.add_layout_image(
#                     dict(
#                         source=logo,
#                         x=np.array(team_x[0]),
#                         y=np.array(team_y[0]),
#                     ))
#         plot.update_layout_images(dict(
#                 xref="x",
#                 yref="y",
#                 sizex=1,
#                 sizey=1,
#                 xanchor='center',
#                 yanchor='middle'
#         ))
#     else:
#         plot = px.scatter_3d(df, x=xaxis, y=yaxis, z=zaxis, color="Team", color_discrete_map=teamcolors)
#
#     def f(row):
#         logo = app.get_asset_url('logos/' + str(row['id']) + '.svg')
#         return '![{0}]({0}#thumbnail)'.format(logo)
#     df.insert(loc=0, column='', value=df.apply(f, axis=1))
#     df = df[["", "Team", "Age", "Height", "Weight"]]
#     columns=[{'id': c, 'name': c} if c != '' else {'name': c, 'id':c, 'type':'text', 'presentation':'markdown'} for c in df.columns]
#     data=df.to_dict('records')
#     return plot, data, columns
