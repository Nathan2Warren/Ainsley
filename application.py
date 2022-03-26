# Python packages
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

# Own packages (must be in same directory as index.py)
from app import app, server
from views import home, page1, page2

server = app.server

CONTENT_STYLE_DIV = {
    "margin": "auto",
    "padding": "2rem 1rem",
    "max-width": "100%",
    "max-height": "10%",
}

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
        dbc.Navbar(
            html.Div(
                [
                    dbc.NavbarBrand(
                        [
                            html.Img(
                                src="assets/navbar_logo.png",
                                height="30px",
                                className="d-inline-block align-top",
                            ),
                            " Ainsley Report",
                        ],
                        className="ml-2",
                        external_link=False,
                        href="/",
                    ),
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "Profile Explorer",
                                    href="/page1",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "About",
                                    href="/page2",
                                    active="exact",
                                )
                            ),
                        ],
                        className="nav-pills",
                    ),
                ],
                className="container",
            ),
            sticky="left",
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", className="container pt-5", style=CONTENT_STYLE_DIV),
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
    else:
        return html.Div(
            [html.H1("404: Page Not Found", className="jumbotron-heading")],
            style={"textAlign": "center", "margin-top": 255},
        )


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
