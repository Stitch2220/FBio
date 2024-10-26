import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

# Create random data with numpy
np.random.seed(1)

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                          mode='lines',
                          name='lines'))

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Random Data Plot"),
    dcc.Graph(
        id='random-data-plot',
        figure=fig  # Use the created Plotly figure
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)