################################################
#
# HOJA DE BALANCE DEL B.C.R.A
#
################################################


# Libraries
import streamlit as st
import json
import datetime 
import pandas as pd

from src.funciones import downloadFile
from src.funciones import selectElementsDict
from src.dataContent import dataContent
from src.mapping.mapBalanceBCRA import SHEET_NAMES
from src.mapping.mapBalanceBCRA import TIPOS
from src.mapping.mapBalanceBCRA import CURRENCIES
from src.mapping.mapBalanceBCRA import SECTORS
from src.mapping.mapBalanceBCRA import FUENTE
from src.mapping.filtrosTemporales import FILTROS_TEMPORALES, FECHAS_ESPECIALES


# CONSTANTES

HOURS_TO_DOWNLOAD = 1

# Config de la pagina
st.set_page_config(page_title="Balance del BCRA")
st.title('Balance del B.C.R.A.')
# st.write('<TODO DESCRIPCION DE LA PAGINA>')

with open('data/configArchivos.json', 'r') as file:
    # Carga el contenido del archivo JSON en un diccionario
    files = json.load(file)

### DESCARGA AUTOMATICA DE LOS ARCHIVOS DEL BCRA ###
for k in files.keys():
    downloadFile(
        url=files[k]['url'],
        filename=files[k]['filename'],
        hours=HOURS_TO_DOWNLOAD,
        return_msg=False,
        )

# Carga el contenido en Cache
@st.cache_data(show_spinner=False)
def cargarContenido(filename: str):
    return dataContent(filename)

with st.spinner('Procesando la hoja de balance del BCRA...'):
    data = cargarContenido(files['balance_sheet']['filename'])

# Se genera la sidebar
st.sidebar.header("Secciones")
st.sidebar.write('Información hasta ', data.getRangeDate()[1])

# 1) SECCION - VISUALIZADOR DE STOCKS
st.header('1. Stocks')
with st.container(border=True):
    whereSel = st.multiselect('Fuente de información', FUENTE.values(), default='Base Monetaria')
    sectorSel = st.multiselect('Sector', SECTORS.values(), default='Total')
    currencySel = st.multiselect('Moneda', CURRENCIES.values(), default='(ARS) Pesos Argentinos')
    customStocks = {
        'where': selectElementsDict(FUENTE, whereSel, False), 
        'sector': selectElementsDict(SECTORS, sectorSel, False), 
        'tipo':['stock', 'indice'], 
        'currency': selectElementsDict(CURRENCIES, currencySel, False), 
    }
    #st.divider()

    # Filtro de fechas
    enable_dates = st.checkbox("Filtar por fecha")
    filtro_fecha = dict()
    # Si el checkbox está marcado, mostrar el selector de fechas
    if enable_dates:
        customFecha = st.selectbox('Filtro de fechas:', FILTROS_TEMPORALES.keys())
        if customFecha == 'Personalizada':
            with st.container(border=True):
                startDate = st.date_input("Inicio", data.getRangeDate()[0])
                endDate = st.date_input("Fin", data.getRangeDate()[1])
                filtro_fecha = {'start': pd.to_datetime(startDate), 'end': pd.to_datetime(endDate)}
        else:
            filtro_fecha = FECHAS_ESPECIALES[FILTROS_TEMPORALES[customFecha]]
    #st.divider()
    
    # Base 100
    base_100 = st.checkbox("Base 100")

# Data de Stocks
st.dataframe(
    data.getStocks(**customStocks, filtro_fecha=filtro_fecha, base_100=base_100)
)

# DISCLAIMER
st.caption('_Toda la información que se muestra proviene exclusivamente de la hoja del balance del Banco Central de la República Argentina._')


