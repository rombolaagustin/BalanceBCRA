################################################
#
# HOJA DE BALANCE DEL B.C.R.A
#
################################################


# Libraries
import streamlit as st
import json
import pandas as pd
import plotly.express as px

from src.funciones import downloadFile
from src.funciones import selectElementsDict
from src.dataContent import dataContent
from datetime import datetime, timedelta, date

# CONSTANTES
from src.mapping.mapBalanceBCRA import CURRENCIES
from src.mapping.mapBalanceBCRA import SECTORS
from src.mapping.mapBalanceBCRA import FUENTE
from src.mapping.filtrosTemporales import FILTROS_TEMPORALES
from src.mapping.filtrosTemporales import FECHAS_ESPECIALES
from src.mapping.filtrosTemporales import VARIACIONES
from src.mapping.filtrosTemporales import MONTHS
from src.mapping.fullColumnsNames import FULL_COLUMNS_NAMES
from src.mapping.metrics import cols_metrics_diaria

# Cargar los nombres de los archivos
with open('data/configArchivos.json', 'r') as file:
    # Carga el contenido del archivo JSON en un diccionario
    files = json.load(file)

# Config de la pagina
st.set_page_config(page_title="Balance del BCRA")
st.title('Balance del B.C.R.A.')
# st.write('<TODO DESCRIPCION DE LA PAGINA>')

# Cache para descargar los archivos
@st.cache_resource(ttl=3600/2)
def downloadAllFiles(files: dict):
    for k in files.keys():
        downloadFile(
            url=files[k]['url'],
            filename=files[k]['filename'],
            hours=files[k]['time_to_download'],
            return_msg=False,
            )

# Carga el contenido en Cache
@st.cache_data(show_spinner=False, ttl=3600/2) # Media Hora 
def cargarContenido(filenames):
    data = dataContent(files['balance_sheet']['filename'], files['cer']['filename'])
    data.generarITCRM(files['itcrm']['filename'])
    return data

#### SE DESCARGAN LOS ARCHIVOS Y SE PROCESA LA HOJA DE BALANCE ####
with st.spinner('Procesando la hoja de balance del BCRA...'):
    downloadAllFiles(files)
    data = cargarContenido(files)

# Se obtienen las fechas min y max
minDate, maxDate = data.getRangeDate()

# Se genera la sidebar
st.sidebar.header("Información")
st.sidebar.write('Información hasta ', maxDate)

# 1) SECCION - VISUALIZADOR DE STOCKS
st.header('1. Stocks')
with st.container(border=True):
    whereSel = st.multiselect(
        label='Fuente de información', 
        options=FUENTE.values(), 
        default=['Base Monetaria', 'Indices', 'Agregados Monetarios', 'Reservas Internacionales'],
        )
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
    
    # Base 100
    base_100 = st.checkbox("Base 100", value=False)

# Dataframe de Stocks
df_stocks = data.getStocks(**customStocks, filtro_fecha=filtro_fecha, base_100=base_100)
df_stocks_show = df_stocks.copy().rename(columns=FULL_COLUMNS_NAMES)
st.dataframe(df_stocks_show)

# Graficador
show_chart = st.checkbox('Graficar', value=True)
with st.container(border=True):
    # Verificar si se debe mostrar el gráfico
    if show_chart:
        # Multiselect para elegir las columnas a graficar
        cols_plot = [FULL_COLUMNS_NAMES[c] for c in df_stocks.columns]
        sel_cols_human = st.multiselect('Selecciona las columnas', cols_plot)
        #use_CER = st.checkbox('Deflactar usando CER', value=False)
        kind_index = st.selectbox(
            label='Moneda para expresar variables', 
            options=['ARS Nominales', 'ARS deflactados por CER', 'Expresado en TC Oficial'], 
            )
        # sel_cols_human es para visualizar de forma comoda para los usuarios
        if sel_cols_human:
            sel_cols = selectElementsDict(FULL_COLUMNS_NAMES, sel_cols_human, False)
            if kind_index == 'ARS deflactados por CER' and 'indices_CER_total_indice_ars' in df_stocks.columns:
                title_plot_stocks = f'Gráfico de Stocks (Expresado en Millones de ARS del {maxDate})'
                df_stocks_plot = df_stocks.copy()
                for colPlot in sel_cols:
                    if colPlot.split('_')[4] == 'ars': # Solo lo nominado en ars
                        df_stocks_plot[colPlot] = (df_stocks_plot[colPlot]/df_stocks_plot['indices_CER_total_indice_ars'])*df_stocks_plot['indices_CER_total_indice_ars'].max()
            elif kind_index == 'Expresado en TC Oficial' and 'reservas_tipoDeCambio_total_indice_ars' in df_stocks.columns:
                title_plot_stocks = f'Gráfico de Stocks (Expresado en TC Oficial)'
                df_stocks_plot = df_stocks.copy()
                for colPlot in sel_cols:
                    if colPlot.split('_')[4] == 'ars': # Solo lo nominado en ars
                        df_stocks_plot[colPlot] = (df_stocks_plot[colPlot]/df_stocks_plot['reservas_tipoDeCambio_total_indice_ars'])
            else:
                title_plot_stocks = f'Gráfico de Stocks (Expresado en Millones de ARS nominales)'
                df_stocks_plot = df_stocks[sel_cols].copy()
            # Rename para visualizar con el nombre full
            df_stocks_plot = df_stocks_plot.rename(columns=FULL_COLUMNS_NAMES)
            fig_stocks = px.line(
                df_stocks_plot,
                x=None, 
                y=sel_cols_human, 
                title=title_plot_stocks
                )
            st.plotly_chart(fig_stocks)
        else:
            st.warning('Se debe seleccionar al menos una serie para graficar')

# 2) SECCION - ITCRM PLOTS
st.header('2. ITCRM (Índice de Tipo de Cambio Real Multilateral)')
with st.container(border=True):
    sel_cols_itcrm = st.multiselect('Índices de tipo de cambio', data.itcrm.columns, default=data.itcrm.columns[0])
    fig_itcrm = px.line(
        data.itcrm, 
        x=None, 
        y=sel_cols_itcrm, 
        title='Índices de tipo de Cambio Real')
    st.plotly_chart(fig_itcrm)

## 3) VARIACIONES PORCENTALES
    
st.header('3. Variaciones Porcentuales')
with st.container(border=True):
    days_custom = st.selectbox('Variación:', VARIACIONES.keys())
    if days_custom == 'Personalizado':
        days_especial = st.number_input('Días de variación:', min_value=1, max_value=20*365)
        df_varcustom = data.getVarCustom(days=days_especial)
        df_varcustom_show = df_varcustom.rename(columns=FULL_COLUMNS_NAMES)
    else:
        df_varcustom = data.getVarCustom(days=VARIACIONES[days_custom])
        df_varcustom_show = df_varcustom.rename(columns=FULL_COLUMNS_NAMES)
    st.dataframe(df_varcustom_show)
    cols_plot_var = [FULL_COLUMNS_NAMES[c] for c in df_varcustom.columns]
    sel_cols_human_var = st.multiselect('Selecciona para graficar', cols_plot_var)
    if sel_cols_human_var:
        sel_cols_var = selectElementsDict(FULL_COLUMNS_NAMES, sel_cols_human_var, False)
        df_varcustom_plot = df_varcustom[sel_cols_var].copy()
        df_varcustom_plot = df_varcustom_plot.rename(columns=FULL_COLUMNS_NAMES)
        fig_varcustom = px.line(
            df_varcustom_plot,
            x=None, 
            y=sel_cols_human_var, 
            title='Variaciones'
            )
        st.plotly_chart(fig_varcustom)

# 4) VARIACIONES EN LA BASE MONETARIA

st.header('4. Operaciones del BCRA')

tvar1, tvar2, tvar3, tvar4, tvar5 = st.tabs(["Variación Diaria", "Acumulada Mensual", "Acumulada Anual", "Interanual", "Personalizada"])

def makeTabVar(
        subheader: str,
        days: int,
        ):  
    col1, col2, col3, col4 = st.columns(4)
    st.subheader(subheader, divider='green')

    if days == -1: # Custom Date
        init_custom = st.date_input(
            label='Ingrese fecha de inicio:', 
            min_value=minDate, 
            max_value=maxDate,
            value=maxDate-timedelta(days=7),
            )
        days_custom = (maxDate - init_custom).days
    else:
        days_custom = days
    df_var = data.getVarDiariaAcumCustom(days=days_custom)
    df_var_pcte = data.getVarCustom(days=days_custom)
    st.dataframe(df_var)
    st.write(df_var.columns)
    st.subheader(':blue[Base Monetaria]')
    with col1:
        st.metric(
            label='Base Monetaria', 
            value=df_var['baseMonetaria_baseMonetaria_total_varDiaria_ars'].values[-1],
            delta=f"{df_var_pcte['baseMonetaria_total_total_stock_ars'].values[-1]}%",
        )

    st.subheader(':blue[Reservas]')


with tvar1:
    makeTabVar(
        subheader=f"Variación Diaria",
        days=1,
    )
with tvar2:
    makeTabVar(
        subheader=f"Variación desde incio del mes de {MONTHS[maxDate.month]}",
        days=maxDate.day,
    )
with tvar3:
    ytd_days = (maxDate - date(maxDate.year, 1, 1)).days
    makeTabVar(
        subheader=f"Variación desde inicio del año {maxDate.year}",
        days=ytd_days,
    )
    
with tvar4:
    makeTabVar(
        subheader=f"Variación interanual desde {maxDate-timedelta(days=365)} hasta {maxDate}",
        days=365,
    )

with tvar5:
    makeTabVar(
        subheader="Variación personalizada",
        days=-1,
        )

#st.dataframe(data.getVarDiaria(where=['baseMonetaria'], currency=['ars']))
#st.dataframe(data.getVarDiaria(where=['reservas'], currency=['usd']))

# TEST --->
        
def downloadInfo(data):
    data.stocks.to_csv('plots/stocks.csv')
    data.var_diaria.to_csv('plots/var_diaria.csv')
    print('Data descargada en plots/')
try:   
    if st.secrets['TEST'] == 'True':
        st.sidebar.warning('TEST MODE ON') # Create a button
        button_download_test = st.sidebar.button("Descargar data frames")
        if button_download_test:
            downloadInfo(data)
        
except:
    pass

# DISCLAIMER
st.sidebar.caption('Los datos utilizados provienen exclusivamente de la hoja del balance y de índices publicados por Banco Central de la República Argentina .')

