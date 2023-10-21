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


def title(user_id=None):
    return f"Dashboard page"


def description(user_id=None):
    return f"This page is the dashboard for the user {user_id}"


def layout(user_id=None):
    solar_service = SolarPlateService()
    data = solar_service.getData(user_id=user_id[1])
    gen_1 = pd.read_csv("/home/python/app/code/content/Plant_1_Generation_Data.csv")
    sens_1 = pd.read_csv(
        "/home/python/app/code/content/Plant_1_Weather_Sensor_Data.csv"
    )
    # format datetime
    gen_1["DATE_TIME"] = pd.to_datetime(gen_1["DATE_TIME"], format="%d-%m-%Y %H:%M")
    sens_1["DATE_TIME"] = pd.to_datetime(
        sens_1["DATE_TIME"], format="%Y-%m-%d %H:%M:%S"
    )

    chart1 = px.line(
        data_frame=gen_1, x="DATE_TIME", y="DAILY_YIELD", title="Daily Yield"
    )
    chart1.update(layout=dict(title=dict(x=0.5)))
    gen_1["HOURS"] = gen_1["DATE_TIME"].dt.time
    chart2 = px.scatter(
        data_frame=gen_1,
        y=["AC_POWER", "DC_POWER"],
        x="HOURS",
        title="Daily Produced AC & DC Power",
    )
    chart2.update(layout=dict(title=dict(x=0.5)))
    gen_1["DATE"] = gen_1["DATE_TIME"].dt.date

    chart3 = px.line(gen_1, x="DATE", y="DAILY_YIELD", title="Daily Yield")
    chart3.update(layout=dict(title=dict(x=0.5)))
    chart4 = px.bar(gen_1, x="DATE", y="TOTAL_YIELD", title="Total Yield")
    chart4.update(layout=dict(title=dict(x=0.5)))
    sens_1["HOURS"] = sens_1["DATE_TIME"].dt.time

    chart5 = px.scatter(
        sens_1, x="HOURS", y="IRRADIATION", title="Irradiation during day hours"
    )
    chart5.update(layout=dict(title=dict(x=0.5)))

    chart6 = px.line(
        sens_1,
        x="DATE_TIME",
        y=["AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE"],
        title="Ambient and Module Temperature",
    )
    chart6.update(layout=dict(title=dict(x=0.5)))

    graph1 = dcc.Graph(id="graph1", figure=chart1, className="img")
    graph2 = dcc.Graph(id="graph2", figure=chart2, className="rectangle")
    graph3 = dcc.Graph(id="graph3", figure=chart3, className="four columns")
    graph4 = dcc.Graph(id="graph4", figure=chart4, className="four columns")
    graph5 = dcc.Graph(id="graph5", figure=chart5, className="rectangle-2")
    graph6 = dcc.Graph(id="graph6", figure=chart6, className="four columns")
    dropdown1 = dcc.Dropdown(id="mydropdown", options=sens_1["HOURS"].unique())

    # setup the header
    header = html.H2(children="Grads Teste")
    # setup to rows, graph 1-3 in the first row, and graph4 in the second:
    row1 = html.Div(children=[graph1, graph2], className="flex bg-gray-50")
    row2 = html.Div(children=[graph3, graph4], className="flex bg-gray-50")

    row3 = html.Div(children=[graph5, graph6], className="flex bg-gray-50")

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
                    row1,
                    row2,
                    row3,
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
