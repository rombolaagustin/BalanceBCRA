################################################
#
# HOJA DE BALANCE DEL B.C.R.A
#
################################################


# Libraries
import streamlit as st
import json

from src.funciones import downloadFile
from src.dataContent import dataContent
from src.mapping.mapBalanceBCRA import SHEET_NAMES, MONEDAS, SECTORES

# CONSTANTES

HOURS_TO_DOWNLOAD = 1

# Config de la pagina
st.set_page_config(page_title="Balance del BCRA")

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

whereSel = st.multiselect('Fuente de información', SHEET_NAMES.values(), default='baseMonetaria')
sectorSel = st.multiselect('Sector', SECTORES, default='total')
currencySel = st.multiselect('Moneda', MONEDAS, default='ars')
customStocks = {
    'where':whereSel, 'sector': sectorSel, 'tipo':['stock', 'indice'], 'currency': currencySel
}

st.dataframe(
    data.getStocks(**customStocks)
)



