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
                    "The homepage shows time series data of users and revenue as well as totals of key metrics.",
                    className="blurb-1",
                ),
                html.P(
                    "The profile explorer is used to quickly find tabulated data from all profiles that have names that are not null.",
                    className="blurb-1",
                ),
            ],
            className="jumbotron text-center",
        ),
        dbc.Row(
            [
                html.H2(
                    "Technology Used",
                    className="lesser-header",
                ),
                dbc.Col(
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
                dbc.Col(
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
                dbc.Col(
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
                    "Further Work",
                    className="jumbotron-heading",
                ),
                html.P(
                    "Collect Feedback: We want to hear from the Lens Community to see if we are collecting and presenting the most useful data, and to make our app the best it can be!",
                    className="blurb-1",
                ),
                html.P(
                    "Front End Improvements: Continue to utilize Finity to improve front end design.",
                    className="blurb-1",
                ),
                html.P(
                    "Profile Explorer: Add a search function and pivot table capability to improve the profile directory usefulness.",
                    className="blurb-1",
                ),
                html.P(
                    "Go Live! We want to deploy this application and on a webserver and present the data when Lens Protocol is on the mainnet",
                    className="blurb-1",
                ),
            ],
            className="jumbotron text-center",
        ),
        dbc.Row(
            [
                html.H2(
                    "Team",
                    className="lesser-header",
                ),
                dbc.Col(
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
                dbc.Col(
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
                dbc.Col(
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
            className="jumbotron text-center",
        ),
    ],
)
