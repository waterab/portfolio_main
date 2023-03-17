import dash
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import os

#path = os.environ.get('DATABASE_URL_POSTGRES')
engine = create_engine("sqlite:///C:\\Users\\WaterDev\\Documents\\GitHub\\portfolio_main\\hockeyviewer\\db_temp\\db2.db")

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = ('Portfolio')
