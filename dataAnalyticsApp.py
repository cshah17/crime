import dash
from dash import html
from dash.dependencies import Output, Input
from dash import dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# read in data
data = pd.read_csv("assets/clean_crime_canada_dataset.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Group 4"

app.layout = dbc.Container(
    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Year"),
                    dbc.CardBody(
                        [
                            html.H4("Select a year", className="card-title"),
                            dcc.Dropdown(
                                id="year-selector",
                                options=[{"label": year, "value": year} for year in data["year"].unique()],
                                value=data["year"].max(),
                                clearable=False
                            ),
                            # html.Hr(),
                            # html.H4("Total number of incidents", className="card-text"),
                            # html.Div(id="incidents-output"),
                        ]
                    ),
                ]),
                md=3,
            ),

            dbc.Col(
                html.Div([
                    html.H4("Total Crimes", className="card-title"),
                    html.P(id="incidents-total"),
                ])
                # dcc.Graph(id="incidents-graph"), md=9
            ),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="incidents-by-region-graph"), md=12),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="incidents-by-type-graph"), md=12),
        ])
    ])
)


# def update_incidents_output(selected_year):
#     incidents = data.loc[data["year"] == selected_year, "incidents"].sum()
#     return f"{incidents}"

# def update_incidents_total(selected_year):
#     incidents_total = data[data["year"] == selected_year]["incidents"].sum()
#     return f"{incidents_total} incidents"


# Define the second callback
@app.callback(
    [
        Output("incidents-total", "children"),
        Output("incidents-by-region-graph", "figure"),
        Output("incidents-by-type-graph", "figure")
    ],
    [
        Input("year-selector", "value")
    ]
)
def update_graphs(selected_year):
    filtered_df = data.loc[data["year"] == selected_year]

    incidents_by_location = filtered_df.groupby("location").sum(numeric_only=True)["incidents"]
    incidents_by_crime_type = filtered_df.groupby("type_of_crime").sum(numeric_only=True)["incidents"]
    # total_incidents = data.loc[data["year"] == selected_year, "incidents"].sum(numeric_only=True)
    incidents_total = data[data["year"] == selected_year]["incidents"].sum(numeric_only=True)
    # return f"{incidents_total} incidents"

    fig1 = px.bar(
        incidents_by_location,
        title=f"Number of Crimes by Location in {selected_year}",
        x=incidents_by_location.index,
        y='incidents',
        labels={
            'location': 'Location',
            'incidents': 'No. of Crimes'
        },
    )
    fig2 = px.bar(
        incidents_by_crime_type,
        title=f"Number of Crimes by Types in {selected_year}",
        x=incidents_by_crime_type.index,
        y='incidents',
        labels={
            'type_of_crime': 'Types of Crime',
            'incidents': 'No. of Crimes'
        })

    # info1 = dbc.Card(
    #     [
    #         dbc.CardHeader("Total Crimes"),
    #         dbc.CardBody(
    #             [
    #                 html.H5("{} incidents".format(total_incidents), className="card-title")
    #             ]
    #         ),
    #     ],
    #     style={"width": "18rem"}
    # )
    return incidents_total, fig1, fig2


#
# def update_incidents_graph(selected_year):
#     filtered_df = data.loc[data["year"] == selected_year]
#     return {
#         "data": [
#             {
#                 "x": filtered_df["year"],
#                 "y": filtered_df["incidents"],
#                 "type": "line",
#                 "name": "Incidents",
#             }
#         ],
#         "layout": {
#             "title": f"Incidents in {selected_year}",
#             "xaxis": {"title": "Year"},
#             "yaxis": {"title": "No. of Crimes"},
#         },
#     }


if __name__ == "__main__":
    app.run_server(debug=True)
