from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dotsama.index import layout as layout_dotsama
from hockeyviewer.index import layout as layout_hockeyviewer
from overview.index import layout as layout_overview

from app import app

server = app.server

# navigation bar for all projects
def navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview", href='/overview')),
            dbc.NavItem(dbc.NavLink("Dotsama", href='/dotsama')),
            dbc.NavItem(dbc.NavLink("NHL Stats", href='/nhlstats'))
        ],
        brand="Austin's Portfolio",
        brand_href="#",
        color="dark",
        dark=True
    )


# main layout
app.title = "Austin's Portfolio"
app.layout = html.Div(
    [
        dcc.Location(id='url'),
        navbar(),
        html.Div(id='page-content')
    ],
    style={'background-color': '#cfd8dc'}
)


# set the content according to the current pathname
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/dotsama":
        return layout_dotsama
    elif pathname == '/nhlstats':
        return layout_hockeyviewer
    else:
        return layout_overview

if __name__ == '__main__':
    app.run_server(debug=True)
