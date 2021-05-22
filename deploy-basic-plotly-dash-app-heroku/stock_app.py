import pandas as pd 
import dash
import dash_html_components as html 
import dash_core_components as dcc 
import plotly.express as px
app = dash.Dash(__name__, title = "Zach's Basic Stock App", suppress_callback_exceptions=True)
server = app.server

df = pd.read_csv('stocks.csv')
df['Date']=pd.to_datetime(df['Date'],format='%Y-%m-%d')
df_hsba = df[df['name']=='HSBA.L'].reset_index()

fig_line = px.line(df_hsba, x = 'Date', y = 'Close')

app.layout = html.Div(
    
    children=[
        html.H1('My basic stock app'),
        html.Div(
            style={'display':'inline-block', 'width':'50%', 'height':'200px', 'float':'left'},
            children=[
                html.H3('Tickers'),
                dcc.Dropdown(
                    id = 'ticker-dropdown',
                    options = [{'label':i, 'value':i} for i in list(df['name'].sort_values(ascending=False).astype(str).unique())],
                    value='HSBA.L', multi=False
                )
            ]

        ),
        html.Div(
            style = {'display':'inline-block', 'width':'70%', 'height':'400px', 'float':'left'},
            children=[
                dcc.Graph(id='trend-stock', figure = fig_line, className = 'viz-line')
            ]
        )
    ]
)

@app.callback(
    dash.dependencies.Output(component_id='trend-stock', component_property='figure'),
    [dash.dependencies.Input(component_id = 'ticker-dropdown', component_property='value')]
)
def update_ticker(tickervalue):
    df = pd.read_csv('stocks.csv')
    df['Date']=pd.to_datetime(df['Date'],format='%Y-%m-%d')
    df = df[df['name']==tickervalue].reset_index()
    fig = px.line(df, x = 'Date', y = 'Close')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)