from dash import dcc, html
from dash.dependencies import Input, Output

from hockeyviewer.nhlscraper import teamcolors
from hockeyviewer.age_weight_height import layout as layout_awh
from hockeyviewer.standings import layout as layout_standings
from app import app

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}


layout = html.Div(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                "NHL STATS"
                            ],
                            className="title",
                            style={
                                "white-space": "nowrap",
                                "line-height": "60px"
                            }
                        )
                    ],
                    className="layout-title")
            ],
            className="layout-header",
            style={
                "display": "flex",
                "flex-flow": "row wrap-reverse",
                "justify-content": "space-between",
                "height": "auto"
            }
        ),
        html.Div(
            [
                dcc.Tabs(id="tabs-hockeyviewer", value='tab-players',
                    children=[
                        dcc.Tab(label='Player Age, Height & Weight', value='tab-players', selected_style=tab_selected_style),
                        #dcc.Tab(label='Standings', value='tab-standings', selected_style=tab_selected_style),
                        #dcc.Tab(label='Player Nationality', value='tab-nationality', selected_style=tab_selected_style),
                        #dcc.Tab(label='Team Shots', value='tab-nationality', selected_style=tab_selected_style)
                    ],
                ),
            ],
            className="layout-tabs"
        ),
        html.Div(id='page-hockeyviewer', style={'padding-left': "15px"})
    ],
    className="ddk-container"
)

# set the content according to the current pathname
@app.callback(Output('page-hockeyviewer', 'children'),
              [Input('tabs-hockeyviewer', 'value')])
def display_page(active_tab):
    if active_tab == 'tab-players':
        return layout_awh
    else:
        return layout_standings
