import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from scipy.optimize import newton

# Acceleration due to gravity (m.s-2); final position of bead (m).
g = 9.81
x2, y2 = 1, 0.65

def cycloid(x2, y2, N=100):
    """Return the path of Brachistochrone curve from (0,0) to (x2, y2).

    The Brachistochrone curve is the path down which a bead will fall without
    friction between two points in the least time (an arc of a cycloid).
    It is returned as an array of N values of (x,y) between (0,0) and (x2,y2).

    """

    # First find theta2 from (x2, y2) numerically (by Newton-Rapheson).
    def f(theta):
        return y2/x2 - (1-np.cos(theta))/(theta-np.sin(theta))
    theta2 = newton(f, np.pi/2)

    # The radius of the circle generating the cycloid.
    R = y2 / (1 - np.cos(theta2))

    theta = np.linspace(0, theta2, N)
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))

    # The time of travel
    T = theta2 * np.sqrt(R / g)
    return x, y, T

def linear(x2, y2, N=100):
    """Return the path of a straight line from (0,0) to (x2, y2)."""

    m = y2 / x2
    x = np.linspace(0, x2, N)
    y = m*x

    # The time of travel
    T = np.sqrt(2*(1+m**2)/g/m * x2)
    print('T(linear) = {:.3f}'.format(T))
    return x, y, T

app = dash.Dash()
server = app.server

# Calculate the cycloid curve
x_cycloid, y_cycloid, T_cycloid = cycloid(1, 1)

# Calculate the straight line
x_line, y_line, T_line = linear(1, 1)

# Create a Plotly scatter plot for the cycloid
cycloid_plot = go.Scatter(x=x_cycloid, y=y_cycloid, mode='lines', name='Cycloid')

# Create a Plotly scatter plot for the straight line
line_plot = go.Scatter(x=x_line, y=y_line, mode='lines', name='Linear')

app.layout = html.Div([
    html.Div([
        html.Label('x2'),
        dcc.Input(id='input-x2', type='number', value=1, min=0.1)
    ]),
    html.Div([
        html.Label('y2'),
        dcc.Input(id='input-y2', type='number', value=1, min=0.1)
    ]),
    dcc.Graph(
        id='cycloid-plot',
        figure={
            'data': [cycloid_plot, line_plot],
            'layout': {
                'yaxis': {
                    'autorange': 'reversed'
                }
            }
        }
    )
])


@app.callback(
    dash.dependencies.Output('cycloid-plot', 'figure'),
    [dash.dependencies.Input('input-x2', 'value'),
     dash.dependencies.Input('input-y2', 'value')],
     
)
def update_plot(x2, y2):
    # Calculate the cycloid curve
    x_cycloid, y_cycloid, T_cycloid = cycloid(x2, y2)

    # Calculate the straight line
    x_line, y_line, T_line = linear(x2, y2)

    # Create a new Plotly scatter plot with lines connecting the points for the cycloid
    cycloid_plot = go.Scatter(x=x_cycloid, y=y_cycloid, mode='lines', name='Braquistocrona')

    # Create a new Plotly scatter plot with lines connecting the points for the straight line
    line_plot = go.Scatter(x=x_line, y=y_line, mode='lines', name='Linear')

    # Add an annotation showing the time of travel for the cycloid
    cycloid_annotation = go.layout.Annotation(text=f'Tempo de Viagem (Braquistocrona): {T_cycloid:.4f}s', x=0.5, y=0.9, xref='paper', yref='paper', showarrow=False, font=dict(size=18), align='center')

    # Add an annotation showing the time of travel for the straight line
    line_annotation = go.layout.Annotation(text=f'Tempo de Viagem (Linear): {T_line:.4f}s', x=0.5, y=0.8, xref='paper', yref='paper', showarrow=False, font=dict(size=18), align='center')

    # Update the figure with the new plots and annotations
    figure = {
        'data': [cycloid_plot, line_plot],
        'layout': {
            'yaxis': {
                'autorange': 'reversed'
            },
            'annotations': [cycloid_annotation, line_annotation]
        }
    }
    
    return figure



if __name__ == '__main__':
    app.run_server()
