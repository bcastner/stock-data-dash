import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd


# Create Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Financial Data Visualization Dashboard"),

    html.Div("Enter Stock Ticker (separated by commas):"),
    dcc.Input(id="stock-tickers", value="AAPL, MSFT", type="text", style={'width': '50%'}),

    html.Div("Select Time Period:"),
    dcc.Dropdown(
        id='time-period',
        options=[
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Month', 'value': '3mo'},
            {'label': '6 Month', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '5 Years', 'value': '5y'},
            {'label': 'Max', 'value': 'max'}
        ],
        value='1mo'
    ),

    dcc.Graph(id='line-chart'),
    dcc.Graph(id='candlestick-chart')
])

# Callback to update graphs based on user input
@app.callback(
    [Output('line-chart', 'figure'),
    Output('candlestick-chart', 'figure')],
    [Input('stock-tickers', 'value'),
     Input('time-period', 'value')]
)
def update_graphs(tickers, period):
    tickers = [ticker.strip().upper() for ticker in tickers.split(',')]

    line_fig = go.Figure()
    candlestick_fig = go.Figure()

    for ticker in tickers:
        # Fetch stock data
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period=period)

        # Create line chart for each stock
        line_fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name=ticker))

        # Add candlestick chart for each stock
        candlestick_fig.add_trace(go.Candlestick(x=hist.index,
                                                 open=hist['Open'],
                                                 high=hist['High'],
                                                 low=hist['Low'],
                                                 close=hist['Close'],
                                                 name=ticker))

        # Create candlestick chart
        candlestick_fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                        open=hist['Open'],
                                                        high=hist['High'],
                                                        low=hist['Low'],
                                                        close=hist['Close'])])

    # Update layout for line chart
    line_fig.update_layout(title=f'Stock Price Comparison (Line Chart)',
                           xaxis_title='Date', yaxis_title='Close Price (USD)')

    # Update layout for candlestick chart
    candlestick_fig.update_layout(title=f'Stock Price Comparison (Candlestick Chart)',
                                  xaxis_title='Date', yaxis_title='Price (USD)')

    return line_fig, candlestick_fig


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
