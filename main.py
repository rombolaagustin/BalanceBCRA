################################################
#
# HOJA DE BALANCE DEL B.C.R.A
#
################################################


# Libraries
import streamlit as st
import json
import datetime 

from src.funciones import downloadFile
from src.dataContent import dataContent
from src.mapping.mapBalanceBCRA import SHEET_NAMES, MONEDAS, SECTORES

# CONSTANTES

HOURS_TO_DOWNLOAD = 1

# Config de la pagina
st.set_page_config(page_title="Balance del BCRA")
st.title('Balance del B.C.R.A.')
### DESCARGA AUTOMATICA DE LOS ARCHIVOS DEL BCRA ###
with open('data/configArchivos.json', 'r') as file:
    # Carga el contenido del archivo JSON en un diccionario
    files = json.load(file)
for k in files.keys():
    downloadFile(
        url=files[k]['url'],
        filename=files[k]['filename'],
        hours=HOURS_TO_DOWNLOAD,
        return_msg=False,
        )

@st.cache_data(show_spinner=False)
def cargarContenido(filename: str):
    return dataContent(filename)

with st.spinner('Procesando la hoja de balance del BCRA...'):
    data = cargarContenido(files['balance_sheet']['filename'])

# 1) VISUALIZADOR DE STOCKS
st.header('Stocks')
with st.container(border=True):
    whereSel = st.multiselect('Fuente de información', SHEET_NAMES.values(), default='baseMonetaria')
    sectorSel = st.multiselect('Sector', SECTORES, default='total')
    currencySel = st.multiselect('Moneda', MONEDAS, default='ars')
    customStocks = {
        'where':whereSel, 'sector': sectorSel, 'tipo':['stock', 'indice'], 'currency': currencySel
    }

enable_dates = st.checkbox("Elegir una fecha como base 100.")

# Si el checkbox está marcado, mostrar el selector de fechas
if enable_dates:
    selected_date = st.date_input("Selecciona una fecha", datetime.date.today())
    st.write("Base 100 en ", selected_date)
else:
    selected_date = None

# Data de Stocks
st.dataframe(
    data.getStocks(**customStocks, fecha_base=selected_date)
)

# DISCLAIMER
st.caption('_Toda la información que se muestra proviene exclusivamente de la hoja del balance del Banco Central de la República Argentina._')


