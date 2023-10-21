from dash import Input, Output, dcc, html, callback
import dash
import pandas as pd
import warnings
import datetime as dt
from dash import Input, Output, dcc, html, callback

warnings.filterwarnings("ignore")
import plotly.express as px
import dash

# html is used to set up the layout, and dcc is used to embed the graphs to the dashboard:
import dash_core_components as dcc
import dash_html_components as html
from dash import Input, Output, callback
from core.services.api.solar_plate_service import SolarPlateService
from datetime import date, datetime


def title(user_id=None):
    return f"Dashboard page"


def description(user_id=None):
    return f"This page is the dashboard for the user {user_id}"


def layout(user_id=None):
    solar_service = SolarPlateService()
    data = solar_service.getData(user_id=str(user_id))
    plate_total = len(data["solar_plates"])
    gen_1 = pd.DataFrame(data["solar_plates"][0]["power_data"])
    # format datetime
    gen_1["event_date"] = pd.to_datetime(
        gen_1["event_date"], format="%Y-%m-%dT%H:%M:%S.%f"
    )

    gen_1["HOURS"] = gen_1["event_date"].dt.time

    gen_1["DATE"] = gen_1["event_date"].dt.date
    gen_1["DAILY_YIELD"] = gen_1["power_delivery_ac"] + gen_1["power_delivery_dc"]
    # Agrupar por dia e calcular a soma de 'DAILY_YIELD'
    daily_yield_by_date = (
        gen_1.groupby(gen_1["event_date"].dt.date)["DAILY_YIELD"].sum().to_dict()
    )
    grouped_dict = []
    for k, v in daily_yield_by_date.items():
        print(k, v)
        grouped_dict.append({"DATE": k, "DAILY_YIELD": v})

    # Criar uma nova coluna 'NEW_COLUMN' com base nos valores de 'daily_yield_by_date'
    gen_1["DAILY_YIELD_BY_DATE"] = gen_1["event_date"].dt.date.map(daily_yield_by_date)

    new_df = pd.DataFrame(grouped_dict)

    chart1 = px.line(
        data_frame=gen_1,
        x="event_date",
        y="DAILY_YIELD_BY_DATE",
        title="Total por momento enviado",
    )
    chart1.update(layout=dict(title=dict(x=0.5)))

    chart2 = px.scatter(
        data_frame=gen_1,
        y=["power_delivery_ac", "power_delivery_dc"],
        x="HOURS",
        title="Daily Produced AC & DC Power",
    )
    chart2.update(layout=dict(title=dict(x=0.5)))

    chart3 = px.line(gen_1, x="DATE", y="DAILY_YIELD", title="Total por dia")
    chart3.update(layout=dict(title=dict(x=0.5)))
    chart4 = px.bar(new_df, x="DATE", y="DAILY_YIELD", title="Total Yield")
    chart4.update(layout=dict(title=dict(x=0.5)))

    graph1 = dcc.Graph(id="graph1", figure=chart1, className="img mt-4 rounded-md")
    graph2 = dcc.Graph(id="graph2", figure=chart2, className="rectangle rounded-md")
    graph3 = dcc.Graph(id="graph3", figure=chart3, className="four columns rounded-md")
    graph4 = dcc.Graph(id="graph4", figure=chart4, className="four columns rounded-md")
    # graph5 = dcc.Graph(id="graph5", figure=chart5, className="rectangle-2")
    # graph6 = dcc.Graph(id="graph6", figure=chart6, className="four columns")
    # dropdown1 = dcc.Dropdown(id="mydropdown", options=sens_1["HOURS"].unique())

    # setup the header
    header = html.H2(children="Grads Teste")

    # check if "b" is none or not.
    today_production = 0
    # datetime_object = datetime.strptime("2023-07-20", "%Y-%m-%d").date()
    datetime_object = date.today()
    if daily_yield_by_date.get(datetime_object) != None:
        today_production = daily_yield_by_date.get(datetime_object)
    # 2023-07-20
    total = html.Div(
        className="flex bg-gray-100 flex-col w-fit bg-white p-4 shadow-sm rounded-md" , children=[html.H1("Total de produção Diária", className="text-xl"), html.H1(today_production, className="text-blue-500 font-extrabold text-3xl self-end")]
    )
    capacity = html.Div(
        className="flex bg-gray-100 flex-col w-fit ml-16 bg-white p-4 shadow-sm rounded-md", children=[html.H1("Capacidade", className="text-xl"), html.H1(f"{today_production/24}kW/h", className="text-blue-500 font-extrabold text-3xl self-end")]
    )

    return html.Div(
        className="flex bg-gray-100 h-full",
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                className="text-center mt-12",
                                children=[
                                    html.Img(
                                        src="/assets/Grads Logo.png",
                                        className="mx-auto w-48",
                                        alt="logo",
                                    ),
                                ],
                            ),
                        ],
                        className="flex items-center justify-center h-14  p-8 ",
                    ),
                    html.Div(
                        [
                            html.A(
                                [
                                    html.Span(
                                        html.I(className="w-5 h-5"),
                                        className="inline-flex justify-center items-center ml-4",
                                    ),
                                    html.Span(
                                        "Geral",
                                        className="ml-2 text-sm font-bold tracking-wide truncate text-center",
                                    ),
                                ],
                                href="#",
                                className="mt-24 relative text-center flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-indigo-500 pr-6",
                            ),
                        ],
                        className="overflow-y-auto overflow-x-hidden flex-grow ",
                    ),
                ],
                className="h-screen shadow-xl bg-gray-50",
            ),
            html.Div(
                [
                    # html.Div(
                    #     [
                    #         html.H4(
                    #             "Número de placas",
                    #             className="text-bold text-md font-extrabold p-4",
                    #         ),
                    #         html.P(
                    #             "",
                    #             className="text-md p-4",
                    #             id="plate-number",
                    #         ),
                    #     ],
                    #     className="bg-gray-50 shadow-xl",
                    # ),
                    html.Div(
                        className="flex flex-row mx-1 mb-4",
                        children=[total, capacity],
                        style={
                            "maxWidth": "1134px",
                            "maxHeight": "677px",
                        },
                    ),
                    html.Div(
                        className="group mx-1",
                        children=[graph2],
                        style={
                            "maxWidth": "1134px",
                            "maxHeight": "677px",
                        },
                    ),
                    html.Div(
                        className="rectangle-wrapper mx-1",
                        children=[graph1],
                        style={
                            "maxWidth": "1357px",
                            "maxHeight": "677px",
                        },
                    ),
                    # html.Div(
                    #     className="img-wrapper",
                    #     children=[graph3],
                    #     style={
                    #         "maxWidth": "1357px",
                    #         "maxHeight": "517px",
                    #     },
                    # ),
                    html.Div(
                        className="img-wrapper mx-1",
                        children=[graph4],
                        style={
                            "maxWidth": "1357px",
                            "maxHeight": "517px",
                        },
                    ),
                ],
                className="w-full h-screen p-32",
            ),
        ],
    )


dash.register_page(
    "dashboard",
    path_template="/dashboard/<user_id>",
    title=title,
    description=description,
    layout=layout,
)
