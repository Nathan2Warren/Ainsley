from datetime import datetime as dt
from datetime import timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table as dtt
from dash import dcc, html
from dash.dependencies import Input, Output

import data_fetcher as f
from app import app

df = f.GraphQLClient._get_data_for_all_profiles(normalize=True)
df = df[df["name"].notna()]
df = df[["id", "name", "bio", "location", "website", "ownedBy"]]
df = df.rename(
    columns={
        "id": "ID",
        "name": "Name",
        "bio": "Bio",
        "location": "Location",
        "website": "Website",
        "ownedBy": "Owned By",
    }
)

layout = (
    dtt.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_header={"backgroundColor": "#8247E5", "fontWeight": "bold", "color": "white"},
        style_table={"overflowX": "auto"},
        style_cell={
            "height": "auto",
            # all three widths are needed
            "minWidth": "180px",
            "width": "180px",
            "maxWidth": "180px",
            "whiteSpace": "normal",
            "backgroundColor": "#DCD5FF",
        },
    ),
)


# layout = (
#     dbc.Container(
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dtt.DataTable(
#                         data=df.to_dict,
#                         columns=[{"name": i, "id": i} for i in df.columns],
#                         style_header={"backgroundColor": "#CF7575"},
#                         style_cell={"backgroundColor": "#CF7575", "color": "white"},
#                     ),
#                     width=12,
#                 ),
#             ],
#         ),
#     ),
# )
