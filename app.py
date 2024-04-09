import streamlit as st
import pandas as pd
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

countries = ['Brazil', 'United States']
intervals = ['Daily', 'Weekly', 'Monthly']
start_date = datetime.today() - timedelta(days=30)
end_date = datetime.today()

@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date, to_date=to_date, interval=interval)
    return df

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

###                SIDEBAR

barra_lateral = st.sidebar.empty()

country_select = st.sidebar.selectbox("Selecione o país:", countries)

acoes_info = ip.get_stocks(country=country_select)
acoes = [{'name': row['name'], 'symbol': row['symbol']} for index, row in acoes_info.iterrows()]

stock_select = st.sidebar.selectbox("Selecione o ativo:", [f"{acao['name']} ({acao['symbol']})" for acao in acoes])

from_date = st.sidebar.date_input('De:', start_date)
to_date = st.sidebar.date_input('Até:', end_date)

intervals_select = st.sidebar.selectbox('Selecione o intervalo:', intervals)

carregar_dados = st.sidebar.button('Carregar dados')

###               CENTRAL
st.title('Stock Monitor')

st.header('Ações')

st.subheader('Visualização gráfica')

grafico_candle = st.empty()
grafico_line = st.empty()

if from_date > to_date:
    st.sidebar.error('Data de ínicio maior do que data final.')
else:
    selected_ticker = stock_select.split(" (")[1][:-1] 
    df = consultar_acao(selected_ticker, country_select, format_date(from_date), format_date(to_date), intervals_select)
    try:
       fig = plotCandleStick(df)
       grafico_candle.plotly_chart(fig)
       grafico_line.line_chart(df.Close)
            
       if carregar_dados:
          st.subheader('Dados')
          st.dataframe(df)
    except Exception as e:
        print("Erro:", e)
        st.error("Ocorreu um erro ao processar os dados.")
