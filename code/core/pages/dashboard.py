from dash import Input, Output, dcc, html, callback
import dash_bootstrap_components as dbc
import requests
import dash
from core.services.api.auth_service import AuthService

def title(user_id=None):
    return f"Dashboard page"


def description(user_id=None):
    return f"This page is the dashboard for the user {user_id}"

def layout(user_id=None):
    return html.Div(
        className="gradient-form h-screen w-screen p-32 bg-slate-50",
        children=[
            dcc.Location(id='url', refresh=True),
            html.Div(id="login-result"),
            html.Div(
                f"The user requested report ID: {user_id}."
            )
        ],
    )

dash.register_page("dashboard", path_template='/dashboard/<user_id>',title=title,
    description=description, layout=layout,)

@callback(
    Output("login-result", "value"),
    Input('url', 'pathname'),
)
def get_user_data(pathname):
    print("pahtname: ", pathname)
    return pathname



