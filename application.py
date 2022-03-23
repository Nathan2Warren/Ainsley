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

CONTENT_STYLE = {
    "margin": "auto",
    "padding": "2rem 1rem",
    "max-width": "100%",
    "max-height": "10%",
}

app.layout = html.Div(
    [
        dbc.Navbar(
            html.Div(
                [
                    dbc.NavbarBrand(
                        [
                            html.Img(
                                src="assets/lens.ico",
                                height="30px",
                                className="d-inline-block align-top",
                            ),
                            " Lens Dashboard",
                        ],
                        className="ml-2",
                        external_link=False,
                        href="/",
                    ),
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink("Home", href="/", active="exact")
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "page1",
                                    href="/page1",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "page2",
                                    href="/page2",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "page3",
                                    href="/page3",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "page4",
                                    href="/page4",
                                    active="exact",
                                )
                            ),
                        ],
                        className="nav-pills",
                    ),
                ],
                className="container",
            ),
            sticky="top",
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="page-content", className="container pt-5", style=CONTENT_STYLE
        ),
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
    server.run(debug=True, host="0.0.0.0", port="80")
