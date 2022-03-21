# Python packages
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

# Own packages (must be in same directory as index.py)
from app import app
from app import server
import os

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
                            "Dashboard",
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
                                    "1",
                                    href="/1",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "2",
                                    href="/2",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "3",
                                    href="/3",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "4",
                                    href="/4",
                                    active="exact",
                                )
                            ),
                            dbc.NavItem(
                                dbc.NavLink(
                                    "5",
                                    href="/5",
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
        html.Div(id="page-content", className="container pt-5", style=CONTENT_STYLE),
    ],
    className="dash-bootstrap",
)
if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port="80")
