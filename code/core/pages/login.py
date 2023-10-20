from dash import Input, Output, dcc, html, callback
import dash_bootstrap_components as dbc
import requests
import dash
from core.services.api.auth_service import AuthService

def title(asset_id=None, dept_id=None):
    return f"Asset Analysis: {asset_id} {dept_id}"


def description(asset_id=None, dept_id=None):
    return f"This is the AVN Industries Asset Analysis: {asset_id} in {dept_id}"

def layout():
    return html.Div(
        className="gradient-form h-screen w-screen p-32 bg-slate-50",
        children=[
            dcc.Location(id='url', refresh=True),
            html.Div(
                className="container mx-auto h-full",
                children=[
                    html.Div(
                        className="g-6 flex h-full flex-wrap items-center justify-center text-neutral-800",
                        children=[
                            html.Div(
                                className="w-full",
                                children=[
                                    html.Div(
                                        className="block rounded-lg bg-white shadow-lg",
                                        children=[
                                            html.Div(
                                                className="lg:flex lg:flex-wrap",
                                                children=[
                                                    html.Div(
                                                        className="px-4 md:px-0 lg:w-6/12 py-24",
                                                        children=[
                                                            html.Div(
                                                                className="md:mx-6 p-12",
                                                                children=[
                                                                    html.Div(
                                                                        className="text-center",
                                                                        children=[
                                                                            html.Img(
                                                                                src="/assets/Grads Logo.png",
                                                                                className="mx-auto w-48",
                                                                                alt="logo",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Form(
                                                                        className="mt-16",
                                                                        children=[
                                                                            html.P("Faça o Login para ultilizar a aplicação", className="mb-4 text-center"),
                                                                            html.Div( 
                                                                                className="relative mb-4 mt-8",
                                                                                children=[
                                                                                    dcc.Input(
                                                                                        type="text",
                                                                                        id="email-input",
                                                                                        placeholder="Email",
                                                                                        className="peer block min-h-[auto] w-full rounded border-2 bg-transparent px-3 py-[0.32rem] leading-[1.6] outline-none transition-all duration-200 ease-linear",
                                                                                    )
                                                                                ],
                                                                            ),
                                                                            html.Div(
                                                                                className="relative mb-4",
                                                                                children=[
                                                                                    dcc.Input(
                                                                                        type="password",
                                                                                        id="password-input",
                                                                                        placeholder="Senha",
                                                                                        className="peer block min-h-[auto] w-full rounded border-2 bg-transparent px-3 py-[0.32rem] leading-[1.6] outline-none transition-all duration-200 ease-linear",
                                                                                    )
                                                                                ],
                                                                            ),
                                                                            html.Div(
                                                                                className="mb-12 pb-1 pt-1 text-center",
                                                                                children=[
                                                                                    html.Button(
                                                                                        "Log in",
                                                                                        type="button",
                                                                                        id="login-button",
                                                                                        className="mb-3 inline-block w-full rounded px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_rgba(0,0,0,0.2)] transition duration-150 ease-in-out hover:shadow-[0_8px_9px_-4px_rgba(0,0,0,0.1),0_4px_18px_0_rgba(0,0,0,0.2)] focus:shadow-[0_8px_9px_-4px_rgba(0,0,0,0.1),0_4px_18px_0_rgba(0,0,0,0.2)] focus:outline-none focus:ring-0 active:shadow-[0_8px_9px_-4px_rgba(0,0,0,0.1),0_4px_18px_0_rgba(0,0,0,0.2)]",
                                                                                        style={"background": "linear-gradient(90deg, rgba(50,77,255,1) 10%, rgba(134,149,251,1) 100%)"},
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="flex items-center rounded-b-lg lg:w-6/12 lg:rounded-r-lg lg:rounded-bl-none py-24",
                                                        style={"background": "linear-gradient(90deg, rgba(50,77,255,1) 10%, rgba(134,149,251,1) 100%)"},
                                                        children=[
                                                            html.Div(
                                                                className="px-4 py-6 text-white md:mx-6 md:p-12",
                                                                children=[
                                                                    html.H4("Somos mais do que apenas uma empresa, transforme sua Energia Solar em Resultados Tangíveis!", className="text-bold text-3xl font-extrabold"),
                                                                    html.P(
                                                                        "Você fez o investimento sábio em painéis solares para sua casa ou empresa, mas agora, como acompanhar o desempenho e maximizar os benefícios? A solução é mais simples do que você imagina!",
                                                                        className="text-sm font-light mt-4",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(id="login-result")

        ],
    )

dash.register_page("home", path='/',     title=title,
    description=description, layout=layout)

@callback(
    Output('url', 'pathname'),
    Input("login-button", "n_clicks"),
    Input("email-input", "value"),
    Input("password-input", "value")
)
def login(n_clicks, email, password):
    auth_service = AuthService()
    if not n_clicks:
        return None
    
    if n_clicks > 0:
        user_id, auth_token = auth_service.login(username=email, password=password)
        return f"dashboard/{user_id}"



