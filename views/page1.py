import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output

import data_fetcher as fetcher
from app import app

client = fetcher.GraphQLClient()
profile_ids = client.get_existing_profile_ids()
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
                        dcc.Graph(id="post_history", config={"displayModeBar": False}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="post_history", config={"displayModeBar": False}),
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
    Output("post_history", "figure"),
    [
        Input("profile_options", "value"),
    ],
)
def update_post_history_graph(profile_id):

    df = pd.json_normalize(client.get_publications(profile_id=profile_id))
    df["createdAt"] = pd.to_datetime(df["createdAt"])
    counts = df.groupby([pd.Grouper(key="createdAt", freq="D")]).size()

    fig = go.Figure([go.Bar(x=df["createdAt"], y=counts)])
    fig.update_layout(
        template="simple_white",
        margin=dict(t=35, b=0, l=0, r=0),
    )
    fig.layout.plot_bgcolor = "#fff"
    fig.layout.paper_bgcolor = "#fff"

    return fig
