import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from scipy.optimize import newton


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Poppins:wght@300;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Brachistochrone"

# Aceleração da gravidade (m.s-2) e número de pontos na curva
g = 9.81
N = 100

def braquistocrona(final_x, final_y, N=100):
    """Retorna o caminho da curva braquistocrona de (0,0) até (final_x, final_y).

    A curva braquistocrona é o caminho pelo qual uma partícula cairá sem atrito entre dois pontos no menor tempo (um arco de uma cicloide).
    É retornado como uma matriz de N valores de (x,y) entre (0,0) e (final_x,final_y).

    """
    # Encontra o parametro (final_theta) formado pelo eixo x e a tangente da curva no ponto final (final_x, final_y) numericamente usando o método de Newton-Rapheson
    def f(theta):
        return final_y/final_x - (1-np.cos(theta))/(theta-np.sin(theta))
    final_theta = newton(f, np.pi/2)

    # Calcula o raio do círculo que gera a cicloide com base em final_theta
    R = final_y / (1 - np.cos(final_theta))

    # Gera N pontos da curva igualmente espaçados em N intervalos entre 0 e final_theta
    theta = np.linspace(0, final_theta, N)

    # Calcula todos os pontos da curva 
    x = R * (theta - np.sin(theta))
    y = R * (1 - np.cos(theta))


    # Calcula o tempo de viagem ao longo da curva
    if final_theta == np.pi:
        T = np.pi * np.sqrt(R / g)
    else:
        T = final_theta * np.sqrt(R / g)
    
    return x, y, T

def linear(final_x, final_y, N=100):
    """Retorna o caminho de uma reta de (0,0) para (final_x, final_y)."""
    
    # Calcula a inclinação da reta
    m = final_y / final_x
    
    # Cria um array de valores uniformemente espaçados de 0 a final_x
    x = np.linspace(0, final_x, N)
    
    # Calcula os valores y correspondentes da reta
    y = m*x
    
    # Calcula o tempo de viagem na reta 
    T = np.sqrt(2*(1+m**2)/g/m * final_x)
    
    # Saída do tempo de viagem com três casas decimais
    print('T(linear) = {:.3f}'.format(T))
    
    # Retorna os valores de x, y e T
    return x, y, T


# Calcula a curva da cicloide
x_cycloid, y_cycloid, T_cycloid = braquistocrona(1, 1)

# Calcula a reta 
x_line, y_line, T_line = linear(1, 1)

# Cria um gráfico de linha para a cicloide com o Plotly
cycloid_plot = go.Scatter(x=x_cycloid, y=y_cycloid, mode='lines', name='Cycloid')

# Cria um gráfico de linha para a reta com o Plotly
line_plot = go.Scatter(x=x_line, y=y_line, mode='lines', name='Linear')

app.layout = html.Div([
    html.Div([html.P("Braquistócrona Simulator")], className="header"),
    html.Div([
        html.Label('x final: '),
        dcc.Input(id='input-final_x', type='number', value=1, min=0.001)
    ],className='x2'),
    html.Div([
        html.Label('y final: '),
        dcc.Input(id='input-final_y', type='number', value=1, min=0.001)
    ], className='y2'),
        html.Div([
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
    ], className='cycloid-plot'),
    html.Div([
        html.P("O problema da braquistócrona é um dos problemas mais notórios das ciências físicas e matemáticas, foi proposto por Johann Bernoulli em 1696 como um desafio aos grandes matemáticos da época, e consiste em achar a curva ao longo do qual uma partícula sob ação da gravidade desliza sem atrito no menor tempo de um dado ponto P a outro Q, assumindo que P está acima de Q."),
         ], className = "paragraph"),
        html.Div([
        html.P("O simulador acima toma como input as coordenadas do ponto final onde a partícula parará, e retorna a curva linear e da cicloide (braquistocrona) que a partícula descreverá, além do tempo de viagem em ambas as curvas sob a ação da gravidade, sem atrito e sem resistência do ar.")
], className = "paragraph"),
html.Div([
        html.P("Alunos: Arthur Valls, Bernardo Nunes, João Vitor Alvarenga e Julia Turazzi")
], className = "footer"),
       ])




@app.callback(
    dash.dependencies.Output('cycloid-plot', 'figure'),
    [dash.dependencies.Input('input-final_x', 'value'),
     dash.dependencies.Input('input-final_y', 'value')],
     
)
def update_plot(final_x, final_y):
    # Calcula a curva da cicloide
    x_cycloid, y_cycloid, T_cycloid = braquistocrona(final_x, final_y)

    # Calcula a curva da reta
    x_line, y_line, T_line = linear(final_x, final_y)

    # Cria um novo plot de acordo com o input do usuário
    cycloid_plot = go.Scatter(x=x_cycloid, y=y_cycloid, mode='lines', name='Braquistocrona')
    line_plot = go.Scatter(x=x_line, y=y_line, mode='lines', name='Linear')

    # Adiciona uma anotação que indica o tempo de viagem para a Cicloide e a Reta
    cycloid_annotation = go.layout.Annotation(text=f'Tempo de Viagem (Braquistocrona): {T_cycloid:.4f}s', x=0.5, y=0.9, xref='paper', yref='paper', showarrow=False, font=dict(size=18), align='center')
    line_annotation = go.layout.Annotation(text=f'Tempo de Viagem (Linear): {T_line:.4f}s', x=0.5, y=0.8, xref='paper', yref='paper', showarrow=False, font=dict(size=18), align='center')

    # Atualiza o plot com os novos gráficos e anotações
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


# Inicializa o app
if __name__ == '__main__':
    app.run_server()
