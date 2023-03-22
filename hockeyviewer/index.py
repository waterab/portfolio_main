from dash import dcc, html, Input, Output

from hockeyviewer.nhlscraper import teamcolors
from hockeyviewer.tabs.age_weight_height import layout as layout_awh
from hockeyviewer.tabs.stats_age_weight_height import layout as layout_stats_awh
from hockeyviewer.tabs.project_info import layout as layout_proj_info
from app import app

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}


layout = html.Div(
    [
        html.Div(
            [
                dcc.Tabs(id="tabs-hockeyviewer", value='tab-players',
                    children=[
                        dcc.Tab(label='Player Age, Height & Weight (Current Season)', value='tab-players', selected_style=tab_selected_style),
                        dcc.Tab(label='Stats Vs. Player Attributes (10 Seasons)', value='tab-players-attr', selected_style=tab_selected_style),
                        dcc.Tab(label='Project Info', value='tab-project-info', selected_style=tab_selected_style),
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
    elif active_tab == 'tab-project-info':
        return layout_proj_info
    else:
        return layout_stats_awh
