import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random

# Load your Excel file
df = pd.read_excel(r'N_species_by_EEZ.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout for the app
app.layout = html.Div([
    html.H1("Biodiversity Data"),
    
    # Container for x-axis dropdown and label
    html.Div([
       html.Label("Species1:", style={'right': '10px'}),
        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=random.choice(df.columns),
            multi=False,
            style={'width': '50%'}
        ),
    ], style={'margin-bottom': '10px'}),
    
    # Container for y-axis dropdown and label
    html.Div([
        html.Label("Species2:", style={'right': '10px'}),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns],
            value=random.choice(df.columns),
            multi=False,
            style={'width': '50%'}
        ),
    ], style={'margin-bottom': '10px'}),
    
    # Scatter plot
    dcc.Graph(
        id='scatter-plot',
        style={'height': '78vh'}
    )
])

# Define callback to update scatter plot based on dropdown selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(selected_x, selected_y):
    # Calculate the ratio between y-axis and x-axis attributes and round to one decimal place
    df['Ratio'] = (df[selected_y] / df[selected_x]).round(1)
    
    # Replace NaN values in the 'Ratio' column with a default value (e.g., 1.0)
    df['Ratio'].fillna(1.0, inplace=True)

    # Update scatter plot
    fig = px.scatter(df, x=df[selected_x], y=df[selected_y], size='Ratio',
                     color='WB_Name_ai', title='Biodiversity Data',
                     labels={selected_x: selected_x, selected_y: selected_y, 'WB_Name_ai': 'Country', 'Ratio': 'Ratio'},
                     template='plotly_dark', size_max=30)  # Adjust size_max as needed

    # Show the plot or save it to an HTML file
    fig.show()
    fig.write_html('Ratio.html')


    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

