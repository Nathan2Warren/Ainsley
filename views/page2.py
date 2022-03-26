from dash import html

layout = html.Div(
    [
        html.Section(
            [
                html.H1(
                    "Ainsley Report",
                    className="jumbotron-heading",
                ),
                html.P(
                    "All the best metrics to follow adoption of the Lens Protocol in one place! These metrics are crtical to gauging the health of the social networking protocol.",
                    className="lead text-muted",
                ),
            ],
            className="jumbotron text-center",
        ),
        html.Div(
            [
                html.Img(
                    src="assets/lens.ico",
                    height="300px",
                    className="d-inline-block align-top",
                )
            ],
            style={"textAlign": "center"},
        ),
    ],
)
