import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read processed data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort data
df = df.sort_values("date")

# Create Dash app
app = Dash(__name__)

# App Layout
app.layout = html.Div(

    style={
        "backgroundColor": "#F4F6F9",
        "padding": "30px",
        "fontFamily": "Arial"
    },

    children=[

        # Main Title
        html.H1(
            "Impact of Pink Morsel Price Increase on Sales",
            style={
                "textAlign": "center",
                "color": "#EF476F",
                "marginBottom": "10px",
                "fontWeight": "bold"
            }
        ),

        # Subtitle
        html.P(
            "Interactive sales dashboard analyzing the effect of the January 15, 2021 price increase.",
            style={
                "textAlign": "center",
                "fontSize": "18px",
                "marginBottom": "30px",
                "color": "#555"
            }
        ),

        # Radio Buttons Container
        html.Div(

            children=[

                html.Label(
                    "Select Region:",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "marginRight": "15px"
                    }
                ),

                dcc.RadioItems(

                    id="region-filter",

                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],

                    value="all",

                    inline=True,

                    style={
                        "marginTop": "10px"
                    },

                    inputStyle={
                        "marginRight": "5px",
                        "marginLeft": "15px"
                    }
                )
            ],

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)",
                "marginBottom": "30px"
            }
        ),

        # KPI Cards
        html.Div(

            id="kpi-cards",

            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "30px",
                "marginBottom": "30px"
            }
        ),

        # Business Insight Card
        html.Div(

            children=[

                html.H3(
                    "Business Insight",
                    style={
                        "color": "#EF476F",
                        "marginBottom": "10px"
                    }
                ),

                html.P(
                    "Sales increased significantly after the January 15, 2021 price increase, suggesting strong customer demand despite higher pricing.",
                    style={
                        "fontSize": "18px",
                        "lineHeight": "1.6",
                        "color": "#444"
                    }
                )
            ],

            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)",
                "marginBottom": "30px",
                "textAlign": "center"
            }
        ),

        # Graph Container
        html.Div(

            dcc.Graph(id="sales-chart"),

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)"
            }
        )
    ]
)

# Callback
@app.callback(

    [Output("sales-chart", "figure"),
     Output("kpi-cards", "children")],

    [Input("region-filter", "value")]
)

def update_dashboard(selected_region):

    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # KPI calculations
    before_avg = filtered_df[
        filtered_df["date"] < "2021-01-15"
    ]["sales"].mean()

    after_avg = filtered_df[
        filtered_df["date"] >= "2021-01-15"
    ]["sales"].mean()

    # Create line chart
    fig = px.line(

        filtered_df,

        x="date",
        y="sales",

        color="region" if selected_region == "all" else None,

        title="Pink Morsel Sales Over Time",

        labels={
            "date": "Date",
            "sales": "Sales ($)",
            "region": "Region"
        },

        hover_data={"sales": ":,.2f"}
    )

    # Vertical line
    fig.add_vline(
        x="2021-01-15",
        line_width=3,
        line_dash="dash",
        line_color="#EF476F"
    )

    # Annotation
    fig.add_annotation(
        x="2021-01-15",
        y=filtered_df["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=2
    )

    # Layout styling
    fig.update_layout(
        plot_bgcolor="#F8F9FA",
        paper_bgcolor="white",
        font=dict(size=14),
        title_x=0.5,
        hovermode="x unified"
    )

    # KPI Cards
    cards = [

        html.Div(

            [
                html.H3("Average Sales Before Increase"),
                html.H2(f"${before_avg:,.2f}")
            ],

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)",
                "width": "300px",
                "textAlign": "center"
            }
        ),

        html.Div(

            [
                html.H3("Average Sales After Increase"),
                html.H2(f"${after_avg:,.2f}")
            ],

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)",
                "width": "300px",
                "textAlign": "center"
            }
        )
    ]

    return fig, cards

# Run App
if __name__ == "__main__":
    app.run(debug=True)