import dash_bootstrap_components as dbc
from dash import html

layout = html.Div(
    [
        html.Section(
            [
                html.H1(
                    "Welcome to the Ainsley Report",
                    className="jumbotron-heading",
                ),
                html.P(
                    "All the best metrics to follow adoption of the Lens Protocol in one place! These metrics are crtical to gauging the health of the social networking protocol.",
                    className="blurb-1",
                ),
                html.P(
                    "Come here to see how many new profiles are added to the the network each day, and see the activity of posts, comments, follows, etc.",
                    className="blurb-1",
                ),
            ],
            className="jumbotron text-center",
        ),
        html.Div(
            [
                html.H2(
                    "Technology Used",
                    className="lesser-header",
                ),
                html.Img(
                    src="assets/lens.ico",
                    height="150px",
                    className="d-inline-block align-top",
                ),
                html.Img(
                    src="assets/polygon.png",
                    height="150px",
                    className="d-inline-block align-top",
                ),
                html.Img(
                    src="assets/graphql.png",
                    height="150px",
                    className="d-inline-block align-top",
                ),
            ],
            style={"textAlign": "center"},
        ),
    ],
)
