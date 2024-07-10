import streamlit as st
import pandas as pd
import numpy as np

# Título da aplicação
st.title('Uber pickups in NYC')

# Coluna de data/hora e URL dos dados
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Função para carregar os dados com cache
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Exibindo o status do carregamento dos dados
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

# Exibindo os dados brutos se a checkbox estiver marcada
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Exibindo o histograma do número de pickups por hora
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Slider para selecionar a hora
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Exibindo o mapa dos pickups na hora selecionada
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
