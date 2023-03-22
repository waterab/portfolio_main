from dash import html, dcc, dash_table, Input, Output, State

from app import app, engine

tab_selected_style = {
    'borderTop': '1px solid #242a44',
}

def datasource():
    return html.Div([dcc.Markdown('''
        ## Project GitHub:

        https://github.com/waterab/portfolio_main

        ## NHL Stats Datasource:

        https://gitlab.com/dword4/nhlapi (Documenting the publicly accessible portions of the NHL API)

        * Public API URL's are then translated to JS using requests.
        * Class nhlstats() was then created as a blueprint to access specific data.
        * Current version uses local db. Previous versions utilized PostgresSQL and Redis for live updates (in work).
        * Deployed through Heroku.

        '''),

    ])



layout = html.Div(
    [
        datasource(),
    ]
)
