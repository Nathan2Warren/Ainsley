import datetime
import time
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
                        html.H4("Parameters"),
                        html.Hr(),
                        html.H6("Global Parameters"),
                        # dbc.Label("Date range", html_for="date_picker_range"),
                        # dcc.RangeSlider(
                        #     id="date_picker_range",
                        #     min=unixTimeMillis("2022-03-17"),
                        #     max=unixTimeMillis(str(dt.today())),
                        #     value=["2022-03-17", str(dt.today())],
                        # ),
                        dcc.DatePickerRange(
                            id="date_picker_range",
                            start_date="2022-03-17",
                            end_date=str(dt.today()),
                            with_portal=False,
                            first_day_of_week=0,
                            style={},
                        ),
                        html.Br(),
                        dbc.Row(html.Br()),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H6("Stats"),
                                        html.P(
                                            "Number of Profiles",
                                            style={"font-style": "italic"},
                                        ),
                                        html.P(id="total_profiles"),
                                        html.P(
                                            "Number of Posts",
                                            style={"font-style": "italic"},
                                        ),
                                        html.P(id="total_posts"),
                                        html.P(
                                            "Number of Mirrors",
                                            style={"font-style": "italic"},
                                        ),
                                        html.P(id="total_mirrors"),
                                    ]
                                ),
                            ],
                            color="#A673EF",
                        ),
                    ],
                    className="sidebar",
                    width=2,
                ),
                dbc.Col(
                    [
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
                                        id="timeseries_post_per_user",
                                        children=[
                                            dcc.Graph(
                                                id="timeseries_post_per_user",
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
                    width=5,
                ),
                dbc.Col(
                    [
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
                                    )
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
                                        id="timeseries_revenue",
                                        children=[
                                            dcc.Graph(
                                                id="timeseries_revenue",
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
                    width=5,
                ),
            ],
        ),
        fluid=True,
    ),
)


@app.callback(
    Output("timeseries_new_users", "figure"),
    Output("timeseries_cum_users", "figure"),
    Output("timeseries_post_per_user", "figure"),
    Output("timeseries_revenue", "figure"),
    Output("total_profiles", "children"),
    Output("total_posts", "children"),
    Output("total_mirrors", "children"),
    [
        Input("date_picker_range", "start_date"),
        Input("date_picker_range", "end_date"),
    ],
)
def update_timeseries_users(start, end):
    start_rev = start
    end_rev = end
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
    mask = timeseries["data.globalProtocolStats.totalRevenue"].apply(lambda x: len(x)) > 0
    timeseries_full, timeseries_blank = timeseries[mask], timeseries[~mask]

    revenue = timeseries[timeseries["data.globalProtocolStats.totalRevenue"].apply(lambda x: len(x)) > 0][
        "data.globalProtocolStats.totalRevenue"
    ]
    revenue_df = pd.json_normalize(revenue.apply(lambda x: x[0]))

    # unpack revenue dicts
    new_ts = pd.concat([timeseries_full.reset_index(drop=True), revenue_df.reset_index(drop=True)], axis=1)
    timeseries = pd.concat(
        [new_ts.reset_index(drop=True), timeseries_blank.reset_index(drop=True)], axis=0
    ).sort_values("start")

    timeseries.loc[timeseries["value"].isnull(), "value"] = 0

    timeseries["value"] = timeseries["value"].astype("float64")
    timeseries_cumsum = timeseries.copy()

    cum_sum_list = [
        "data.globalProtocolStats.totalProfiles",
        "data.globalProtocolStats.totalBurntProfiles",
        "data.globalProtocolStats.totalPosts",
        "data.globalProtocolStats.totalMirrors",
        "data.globalProtocolStats.totalComments",
        "data.globalProtocolStats.totalCollects",
        "data.globalProtocolStats.totalFollows",
        "data.globalProtocolStats.totalRevenue",
        "value",
    ]

    for i in cum_sum_list:
        timeseries_cumsum[i] = timeseries_cumsum[i].cumsum()

    # post per user
    timeseries_cumsum["post_per_user"] = (
        timeseries_cumsum["data.globalProtocolStats.totalPosts"]
        / timeseries_cumsum["data.globalProtocolStats.totalProfiles"]
    )

    # Stats/Totals
    total_profiles = timeseries_cumsum.iloc[-1]["data.globalProtocolStats.totalProfiles"]
    total_posts = timeseries_cumsum.iloc[-1]["data.globalProtocolStats.totalPosts"]
    total_mirrors = timeseries_cumsum.iloc[-1]["data.globalProtocolStats.totalMirrors"]

    ### Plots ###

    # new users
    fig_new_users = go.Figure(go.Bar(y=timeseries["data.globalProtocolStats.totalProfiles"], x=timeseries["start"]))
    # cumulative users
    fig_cum_users = go.Figure(
        go.Scatter(y=timeseries_cumsum["data.globalProtocolStats.totalProfiles"], x=timeseries_cumsum["start"])
    )
    # post per user
    fig_post_per_user = go.Figure(
        go.Scatter(y=timeseries_cumsum["post_per_user"], x=timeseries_cumsum["start"]),
    )
    # revenue

    timeseries_revenue = timeseries[~timeseries["asset.symbol"].isnull()]
    timeseries_revenue_grouped = timeseries_revenue.groupby(["start", "end", "asset.symbol"]).sum().reset_index()

    timeseries_revenue_grouped["value"] = timeseries_revenue_grouped["value"].cumsum()

    date_range = pd.DataFrame({"start": pd.date_range(start_rev, end_rev)})
    timeseries_revenue_fixed = pd.merge(date_range, timeseries_revenue_grouped, on="start", how="left")

    timeseries_revenue_fixed["value"] = timeseries_revenue_fixed["value"].fillna(method="ffill")

    fig_revenue = go.Figure(
        go.Scatter(y=timeseries_revenue_fixed["value"], x=timeseries_revenue_fixed["start"]),
    )

    fig_new_users.update_layout(
        yaxis_title="Count",
        xaxis_title="Date",
        title="<b>New Users</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=0),
    )
    fig_cum_users.update_layout(
        yaxis_title="Total Users",
        xaxis_title="Date",
        title="<b>Cumulative Users</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=0),
    )

    fig_post_per_user.update_layout(
        yaxis_title="Posts/User",
        xaxis_title="Date",
        title="<b>Average Posts per User</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=0),
    )

    fig_revenue.update_layout(
        yaxis_title="Cumulative Total",
        xaxis_title="Date",
        title="<b>Cumulative Protocol Revenue</b>",
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=50, b=5, l=70, r=0),
        legend={
            "traceorder": "normal",
            "itemclick": "toggleothers",
            "itemdoubleclick": "toggle",
        },
        legend_title_text="Currency",
    )

    return (
        fig_new_users,
        fig_cum_users,
        fig_post_per_user,
        fig_revenue,
        f"{total_profiles}",
        f"{total_posts}",
        f"{total_mirrors}",
    )
