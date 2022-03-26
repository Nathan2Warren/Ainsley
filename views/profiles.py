from datetime import datetime as dt
from datetime import timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash_table as dtt
from dash.dependencies import Input, Output

import data_fetcher as f
from app import app

profile_ids = f.GraphQLClient.get_existing_profile_ids()
profile_options = [{"label": p_id, "value": p_id} for p_id in profile_ids]


layout = (
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="profile_options",
                            value=profile_options[0]["value"],
                            options=profile_options,
                            style={"width": "60%"},
                            searchable=True,
                            clearable=False,
                        ),
                        dbc.Row(
                            [
                                dcc.Loading(
                                    id="post_history",
                                    children=[
                                        dcc.Graph(
                                            id="post_history",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                    width=6,
                ),
            ],
        ),
    ),
)


@app.callback(
    Output("profile_options", "value"),
    [
        Input("profile_options", "options"),
    ],
)
def update_profile_id_select(profile_options):
    return profile_options[0]["value"]


@app.callback(
    Output("post_history", "children"),
    [
        Input("profile_options", "value"),
    ],
)
def update_post_history_graph(profile_id):

    df = f.GraphQLClient._get_data_for_all_profiles(normalize=True)
    top3_df = dtt.DataTable(
        data=df.to_dict,
        columns=[{"name": i, "id": i} for i in df.columns],
        style_header={"backgroundColor": "#CF7575"},
        style_cell={"backgroundColor": "#CF7575", "color": "white"},
    )

    # fig = go.Figure([go.Bar(x=df["createdAt"], y=counts)])
    # fig.update_layout(
    #     template="simple_white",
    #     margin=dict(t=15, b=5, l=40, r=5),
    # )
    # top3_df.layout.plot_bgcolor = "#fff"
    # top3_df.layout.paper_bgcolor = "#fff"

    return top3_df
