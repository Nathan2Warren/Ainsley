from datetime import datetime as dt
from datetime import timedelta

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
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
                                dbc.Label("Date range", html_for="date_picker_range"),
                                dcc.DatePickerRange(
                                    id="date_picker_range",
                                    start_date="2022-03-17",
                                    end_date=str(dt.today()),
                                    with_portal=False,
                                    first_day_of_week=0,
                                    style={},
                                ),
                            ],
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
                dbc.Col(
                    [
                        html.Br(),
                        dbc.Card(
                            dbc.Col(
                                [
                                    dcc.Loading(
                                        id="timeseries_new_users",
                                        children=[
                                            dcc.Graph(
                                                id="timeseries_new_users",
                                                style={"width": "90%", "height": "80%"},
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                    ),
                                ],
                                align="end",
                                width=12,
                            ),
                            className="align-self-center",
                        ),
                        html.Br(),
                        dbc.Card(
                            dbc.Col(
                                [
                                    dcc.Loading(
                                        id="timeseries_cum_users",
                                        children=[
                                            dcc.Graph(
                                                id="timeseries_cum_users",
                                                style={"width": "90%", "height": "80%"},
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                    )
                                ],
                                align="end",
                                width=12,
                            ),
                            className="align-self-center",
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
    Output("post_history", "figure"),
    [
        Input("profile_options", "value"),
    ],
)
def update_post_history_graph(profile_id):

    df = f.GraphQLClient.get_publications_by_profile(profile_id=profile_id)
    df["createdAt"] = pd.to_datetime(df["createdAt"])
    counts = df.groupby([pd.Grouper(key="createdAt", freq="D")]).size()

    fig = go.Figure([go.Bar(x=df["createdAt"], y=counts)])
    fig.update_layout(
        template="simple_white",
        margin=dict(t=15, b=5, l=40, r=5),
    )
    fig.layout.plot_bgcolor = "#fff"
    fig.layout.paper_bgcolor = "#fff"

    return fig


@app.callback(
    Output("timeseries_new_users", "figure"),
    Output("timeseries_cum_users", "figure"),
    [
        Input("date_picker_range", "start_date"),
        Input("date_picker_range", "end_date"),
    ],
)
def update_timeseries_users(start, end):
    freq = "D"
    start_list = pd.date_range(start, end).tolist()
    end_list = [i + pd.Timedelta(1, unit=freq) for i in start_list]
    start_list = [str(i) for i in start_list]
    end_list = [str(i) for i in end_list]

    dfs = []
    for start, end in zip(start_list, end_list):
        dfs.append(f.GraphQLClient.get_timeseries(start=start, end=end))

    timeseries = pd.concat(dfs)
    timeseries["start"] = pd.to_datetime(timeseries["start"])
    timeseries_cumsum = pd.concat([timeseries.iloc[:, :-3].cumsum(), timeseries.iloc[:, -3:]], axis=1)
    # new users
    fig_new_users = go.Figure(go.Bar(y=timeseries["data.globalProtocolStats.totalProfiles"], x=timeseries["start"]))
    # cumulative users
    fig_cum_users = go.Figure(
        go.Scatter(y=timeseries_cumsum["data.globalProtocolStats.totalProfiles"], x=timeseries_cumsum["start"])
    )

    fig_new_users.update_layout(
        yaxis_title="Count",
        xaxis_title="Date",
        title="<b>New Users</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=-0),
    )
    fig_cum_users.update_layout(
        yaxis_title="Total Users",
        xaxis_title="Date",
        title="<b>Cumulative Users</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=0),
    )

    return fig_new_users, fig_cum_users
