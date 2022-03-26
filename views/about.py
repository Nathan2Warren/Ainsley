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
        html.Section(
            [
                html.H2(
                    "Technology Used",
                    className="lesser-header",
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/lens.ico",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "Lens API",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Pull data from API requests for global stats and individual profiles",
                            className="blurb",
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/polygon.png",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "Polygon Finity",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Selected beautiful, logos, buttons, and styles from the Finity figma file.",
                            className="blurb",
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/graphql.png",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "GraphQL",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Data query language used to collect key metrics from the API and present it on a web page",
                            className="blurb",
                        ),
                    ],
                ),
            ],
            style={"textAlign": "center"},
        ),
        html.Section(
            [
                html.H2(
                    "About",
                    className="lesser-header",
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/trashman.png",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "Matthew Healy",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Data Engineer",
                            className="blurb",
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/benSnow.png",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "Benjamin Scheinberg",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Engineer",
                            className="blurb",
                        ),
                    ],
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/nate_smile.png",
                            height="150px",
                            className="d-inline-block align-top",
                        ),
                        html.H3(
                            "Nathan Warren",
                            className="jumbotron-heading",
                        ),
                        html.P(
                            "Data Scientist",
                            className="blurb",
                        ),
                    ],
                ),
            ],
        ),
    ],
)
