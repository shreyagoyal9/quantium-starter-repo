import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Read processed data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")

# Calculate average sales before and after price increase
before_avg = df[df["date"] < "2021-01-15"]["sales"].mean()
after_avg = df[df["date"] >= "2021-01-15"]["sales"].mean()

# Create line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Sales ($)",
        "region": "Region"
    },
    hover_data={"sales": ":,.2f"}
)

# Add vertical line for price increase
fig.add_vline(
    x="2021-01-15",
    line_width=3,
    line_dash="dash",
    line_color="red"
)

# Add annotation
fig.add_annotation(
    x="2021-01-15",
    y=df["sales"].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=2
)

# Improve layout
fig.update_layout(
    plot_bgcolor="#F8F9FA",
    paper_bgcolor="white",
    font=dict(size=14),
    title_x=0.5
)

# Create Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={
        "backgroundColor": "#F4F6F9",
        "padding": "30px",
        "fontFamily": "Arial"
    },
    children=[

        # Main heading
        html.H1(
            "Impact of Pink Morsel Price Increase on Sales",
            style={
                "textAlign": "center",
                "color": "#EF476F",
                "marginBottom": "10px"
            }
        ),

        # Subtitle
        html.P(
            "Sales increased significantly after the January 15, 2021 price increase.",
            style={
                "textAlign": "center",
                "fontSize": "18px",
                "marginBottom": "30px",
                "color": "#555"
            }
        ),

        # KPI Cards
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "30px",
                "marginBottom": "40px"
            },
            children=[

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
                ),
            ]
        ),

        # Graph container
        html.Div(
            dcc.Graph(figure=fig),
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 2px 8px rgba(0,0,0,0.1)"
            }
        )
    ]
)

# Run app
if __name__ == "__main__":
    app.run(debug=True)