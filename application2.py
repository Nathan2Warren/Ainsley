# Python packages
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Own packages (must be in same directory as index.py)
from app import app, server
from views import home, page1, page2, page3, page4

server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE_SIDEBAR = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div(
    [
        html.Div(
            [
                html.H2("Ainsley Report", className="display-4"),
                html.Hr(),
                html.P("text", className="lead"),
                dbc.Nav(
                    [
                        dbc.NavLink("Home", href="/", active="exact"),
                        dbc.NavLink("Page 1", href="/page1", active="exact"),
                        dbc.NavLink("Page 2", href="/page2", active="exact"),
                        dbc.NavLink("Page 3", href="/page3", active="exact"),
                        dbc.NavLink("Page 4", href="/page4", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            style=SIDEBAR_STYLE,
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", className="container pt-5", style=CONTENT_STYLE_SIDEBAR),
    ],
    className="dash-bootstrap",
)


@app.callback(
    Output(component_id="page-content", component_property="children"),
    Input(component_id="url", component_property="pathname"),
)
def display_page(pathname):
    if pathname == "/":
        return home.layout
    if pathname == "/page1":
        return page1.layout
    if pathname == "/page2":
        return page2.layout
    if pathname == "/page3":
        return page3.layout
    if pathname == "/page4":
        return page4.layout
    else:
        return html.Div(
            [html.H1("404: Page Not Found", className="jumbotron-heading")],
            style={"textAlign": "center", "margin-top": 255},
        )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="8080")
