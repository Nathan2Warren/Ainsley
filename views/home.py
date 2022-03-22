import dash_html_components as html

layout = html.Div(
    [
        html.Section(
            [
                html.H1(
                    "Welcome to the Ainsley Report",
                    className="jumbotron-heading",
                ),
                html.P(
                    "Description 1. "
                    "Desc 2 "
                    "Desc 3 "
                    "Desc 4 "
                    "Desc 5 "
                    "Desc 6",
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
