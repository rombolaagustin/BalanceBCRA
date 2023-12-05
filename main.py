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


# CONSTANTES
from src.mapping.mapBalanceBCRA import SHEET_NAMES
from src.mapping.mapBalanceBCRA import TIPOS
from src.mapping.mapBalanceBCRA import CURRENCIES
from src.mapping.mapBalanceBCRA import SECTORS
from src.mapping.mapBalanceBCRA import FUENTE
from src.mapping.filtrosTemporales import FILTROS_TEMPORALES, FECHAS_ESPECIALES

# Config de la pagina
st.set_page_config(page_title="Balance del BCRA")
st.title('Balance del B.C.R.A.')
# st.write('<TODO DESCRIPCION DE LA PAGINA>')

with open('data/configArchivos.json', 'r') as file:
    # Carga el contenido del archivo JSON en un diccionario
    files = json.load(file)

### DESCARGA AUTOMATICA DE LOS ARCHIVOS DEL BCRA ###
@st.cache_resource
def downloadAllFiles(files: dict):
    for k in files.keys():
        downloadFile(
            url=files[k]['url'],
            filename=files[k]['filename'],
            hours=files[k]['time_to_download'],
            return_msg=False,
            )

# Carga el contenido en Cache
@st.cache_data(show_spinner=False)
def cargarContenido(filename: str, filename_cer = ''):
    return dataContent(filename, filename_cer)

with st.spinner('Procesando la hoja de balance del BCRA...'):
    downloadAllFiles(files)
    data = cargarContenido(files['balance_sheet']['filename'], files['cer']['filename'])

minDate, maxDate = data.getRangeDate()

# Se genera la sidebar
st.sidebar.header("Secciones")
st.sidebar.write('Información hasta ', maxDate)

# 1) SECCION - VISUALIZADOR DE STOCKS
st.header('1. Stocks')
with st.container(border=True):
    whereSel = st.multiselect('Fuente de información', FUENTE.values(), default=['Base Monetaria', 'Indices'])
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
    enable_dates = st.checkbox("Filtar por fecha", value=False)
    filtro_fecha = dict()
    # Si el checkbox está marcado, mostrar el selector de fechas
    if enable_dates:
        customFecha = st.selectbox('Filtro de fechas:', FILTROS_TEMPORALES.keys())
        if customFecha == 'Personalizada':
            with st.container(border=True):
                startDate = st.date_input(
                    label="Inicio", 
                    value=minDate, 
                    min_value=minDate,
                    max_value=maxDate,
                    )
                endDate = st.date_input(
                    label="Fin", 
                    value=maxDate, 
                    min_value=minDate,
                    max_value=maxDate,
                    )
                filtro_fecha = {'start': pd.to_datetime(startDate), 'end': pd.to_datetime(endDate)}
        else:
            filtro_fecha = FECHAS_ESPECIALES[FILTROS_TEMPORALES[customFecha]]
    #st.divider()
    
    # Base 100
    base_100 = st.checkbox("Base 100", value=False)

# Data de Stocks
df_stocks = data.getStocks(**customStocks, filtro_fecha=filtro_fecha, base_100=base_100)
st.dataframe(df_stocks)
# Graficador
show_chart = st.checkbox('Graficar', value=True)

with st.container(border=True):
    
    # Verificar si se debe mostrar el gráfico
    if show_chart:
        # Multiselect para elegir las columnas a graficar
        sel_cols = st.multiselect('Selecciona las columnas', df_stocks.columns)
        use_CER = st.checkbox('Deflactar usando CER', value=False)
        if sel_cols:
            if use_CER and 'indices_CER_total_indice_ars' in df_stocks.columns:
                df_stocks_plot = df_stocks.copy()
                for colPlot in sel_cols:
                    if colPlot.split('_')[4] == 'ars': # Solo lo nominado en ars
                        
                        df_stocks_plot[colPlot] = (df_stocks_plot[colPlot]/df_stocks_plot['indices_CER_total_indice_ars'])*df_stocks_plot['indices_CER_total_indice_ars'].max()
            else:
                df_stocks_plot = df_stocks[sel_cols].copy()
            st.subheader('Gráfico')
            st.line_chart(
                data=df_stocks_plot,
                x=None, # None use the index
                y=sel_cols,
            )
        else:
            st.warning('Se debe seleccionar al menos una serie para graficar')
    

# DISCLAIMER
st.caption('_Toda la información que se muestra proviene exclusivamente de la hoja del balance del Banco Central de la República Argentina._')


