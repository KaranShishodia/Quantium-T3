from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# 1. Load the processed data
df = pd.read_csv('formatted_data.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

# 2. Initialize the Dash app
app = Dash(__name__)

# 3. Define the Layout
app.layout = html.Div(style={'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    # Header
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Region Picker (Radio Items)
    html.Div([
        html.Label("Select Region: ", style={'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='region-picker',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True,
            style={'padding': '10px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Line Chart
    dcc.Graph(id='sales-line-chart')
])

# 4. Callback for Interactivity
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    # Filter data based on selection
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Create the chart
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Pink Morsel Sales: {selected_region.capitalize()} Region",
        labels={"sales": "Total Sales ($)", "date": "Date"}
    )
    
    # Add a vertical line for the price increase date (Jan 15, 2021)
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="red", 
                  annotation_text="Price Increase")
    
    fig.update_layout(transition_duration=500)
    return fig

# 5. Run the app
if __name__ == '__main__':
    app.run(debug=True)