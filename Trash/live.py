import dash
import serial
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import time

# Global variables
emg_value = 0  # This will be updated by the Arduino thread
lock = threading.Lock()  # Create a lock for thread-safe access

# Function to read data from Arduino
def read_arduino_data():
    global emg_value
    emg_value = 4  # Placeholder value for testing
    arduino_port = 'COM4'  # Replace with your Arduino port
    baud_rate = 500000
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)  # Allow time for the connection to establish
        print("Serial connection established.")
        ser.close()
    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
        return

    try:
        while True:
            new_value = ser.readline().decode('utf-8').strip()
            emg_value = float(new_value)  # Convert value to float
    except Exception as e:
        print(f"Error reading from Arduino: {e}")


# Start the thread for reading Arduino data
read_arduino_data()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div(
    children=[
        html.H1("Live EMG Data Stream"),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1000, n_intervals=0)  # Update every second
    ]
)

# Initialize lists to store data
data = []
time_data = []
start_time = time.time()

# Callback to update the graph
@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n):
    global data, time_data, emg_value

    # Acquire the lock before accessing the shared resource
    new_value = emg_value

    # Update time and data
    current_time = time.time() - start_time
    data.append(new_value)
    time_data.append(current_time)

    # Limit to 1000 samples (last second of data)
    if len(data) > 1000:
        data = data[-1000:]
        time_data = time_data[-1000:]

    # Create the figure for Plotly
    figure = go.Figure(
        data=[go.Scatter(x=list(time_data), y=list(data), mode='lines', name='EMG Signal')],
        layout=go.Layout(
            title='Real-Time EMG Signal',
            xaxis=dict(title='Time (s)', range=[max(0, current_time - 1), current_time]),
            yaxis=dict(title='Signal Amplitude'),
            showlegend=True
        )
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)


