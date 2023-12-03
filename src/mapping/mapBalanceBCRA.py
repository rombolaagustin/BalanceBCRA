##### Mapping para leer el excel del BCRA #####
"""
- El excel contiene muchas columnas que se deben eliminar, las mismas se llaman deleteX donde X es el numero de columna
- Las columnas utiles (excepto la fecha) tiene el siguiente formato de nomenclatura:
--> NOMBRE_SECTOR_TIPO_MONEDA
Ejemplo: baseMonetaria_varDiaria_ars
"""

# Tipos 
TIPOS = {
    'varDiaria': 'Variaciones Diarias',
    'stock': 'Stocks',
    'indice': 'Índices',
    'tasa': 'Tasa',
}

# Currencies
CURRENCIES = {
    'ars': '(ARS) Pesos Argentinos',
    'usd': '(USD) Dólares Americanos',
}

# Sector
SECTORS = {
    'pub': 'Sector Público',
    'priv': 'Sector Privado',
    'total': 'Total',
}

# Fuente
FUENTE = {
    'baseMonetaria': 'Base Monetaria', 
    'reservas': 'Reservas Internacionales', 
    'depositos': 'Depósitos', 
    'prestamos': 'Préstamos', 
    'instrumentosBCRA': 'Instrumentos del BCRA',
}

# Hojas del Archivo
SHEET_NAMES = {
    'BASE MONETARIA': 'baseMonetaria', 
    'RESERVAS': 'reservas', 
    'DEPOSITOS': 'depositos', 
    'PRESTAMOS': 'prestamos', 
    'INSTRUMENTOS DEL BCRA': 'instrumentosBCRA',
}

COLUMNS_NAMES = {
    'BASE MONETARIA': [
        'date',
        'delete1',
        'baseMonetaria_total_varDiaria_ars',
        'divisasSectorPublico_total_varDiaria_ars',
        'divisasTesoroNaciona_total_varDiaria_ars',
        'adelantosTesoro_total_varDiaria_ars',
        'transfUtilidades_total_varDiaria_ars',
        'resto_total_varDiaria_ars',
        'pases_total_varDiaria_ars',
        'leliqs_total_varDiaria_ars',
        'redescuentos_total_varDiaria_ars',
        'interesesPasivos_total_varDiaria_ars',
        'lebacs_total_varDiaria_ars',
        'rescateCuasimonedas_total_varDiaria_ars',
        'otrasOperaciones_total_varDiaria_ars',
        'delete2',
        'billetesPublico_total_varDiaria_ars',
        'billetesEntidades_total_varDiaria_ars',
        'cheques_total_varDiaria_ars',
        'ctaCorrienteBCRA_total_varDiaria_ars',
        'totalSinCuasi_total_varDiaria_ars',
        'cuasimonedas_total_varDiaria_ars',
        'total_total_varDiaria_ars',
        'delete3',

        'billetesPublico_total_stock_ars',
        'billetesEntidades_total_stock_ars',
        'cheques_total_stock_ars',
        'ctaCorrienteBCRA_total_stock_ars',
        'totalSinCuasi_total_stock_ars',
        'cuasimonedas_total_stock_ars',
        'total_total_stock_ars',
        'tipoSerie',
    ],
    'RESERVAS': [
        'date',
        'delete1',
        'total_total_stock_usd',
        'oroDivisas_total_stock_usd',
        'pasePasivoExterior_total_stock_usd',
        'delete2',
        'total_total_varDiaria_usd',
        'compraDivisas_total_varDiaria_usd',
        'orgInt_total_varDiaria_usd',
        'operacionesSectorPublico_total_varDiaria_usd',
        'efectivoMinimo_total_varDiaria_usd',
        'otros_total_varDiaria_usd',
        'delete3',
        'deg_total_stock_usd',
        'delete4',
        'tipoDeCambio_total_indice_ars',
        'tipoSerie',
    ],
    'DEPOSITOS': [
        'date',
        'ctaCorriente_total_stock_ars',
        'cajaAhorro_total_stock_ars',
        'PFTradicional_total_stock_ars',
        'PFUVA_total_stock_ars',
        'otrosDepositos_total_stock_ars',
        'cedros_total_stock_ars',
        'depSinBoden_total_stock_ars',
        'boden_total_stock_ars',
        'depositos_total_stock_ars',
        'ctaCorriente_priv_stock_ars',
        'cajaAhorro_priv_stock_ars',
        'PFTradicional_priv_stock_ars',
        'PFUVA_priv_stock_ars',
        'otrosDepositos_priv_stock_ars',
        'cedros_priv_stock_ars',
        'depSinBoden_priv_stock_ars',
        'boden_priv_stock_ars',
        'depositos_priv_stock_ars',
        'delete1', 
        'delete2',
        'delete3',
        'delete4',
        'delete5',
        'delete6',
        'depositos_total_stock_usd',
        'depositos_priv_stock_usd',
        'delete7',
        'm2_total_stock_ars', 
        'tipoSerie',
    ],
    'PRESTAMOS': [
        'date',
        'adelantos_priv_stock_ars',
        'documentos_priv_stock_ars',
        'hipotecarios_priv_stock_ars',
        'prendarios_priv_stock_ars',
        'personales_priv_stock_ars',
        'tarjetas_priv_stock_ars',
        'otrosPrestamos_priv_stock_ars',
        'total_priv_stock_ars',
        'adelantos_priv_stock_usd',
        'documentos_priv_stock_usd',
        'hipotecarios_priv_stock_usd',
        'prendarios_priv_stock_usd',
        'personales_priv_stock_usd',
        'tarjetas_priv_stock_usd',
        'otrosPrestamos_priv_stock_usd',
        'total_priv_stock_usd',
        'delete1',
        'delete2',
        'delete3',
        'delete4',
        'tipoSerie',
    ],
    'INSTRUMENTOS DEL BCRA': [
        'date',
        'pasesPasivos_total_stock_ars',
        'pasesPasivosFCI_total_stock_ars',
        'pasesActivos_total_stock_ars',
        'leliq_total_stock_ars',
        'lebac_total_stock_ars',
        'lebacEntidades_total_stock_ars',
        'lebacUsdLediv_total_stock_usd',
        'nocom_total_stock_ars',
        'polMonTNA_total_tasa_ars',
        'polMonTEA_total_tasa_ars',
        'pasivos1d_total_tasa_ars',
        'pasivos7d_total_tasa_ars',
        'activos1d_total_tasa_ars',
        'activos7d_total_tasa_ars',
        'lebac1m_total_tasa_ars',
        'lebac2m_total_tasa_ars',
        'lebac3m_total_tasa_ars',
        'lebac4m_total_tasa_ars',
        'lebac5m_total_tasa_ars',
        'lebac6m_total_tasa_ars',
        'lebac7m_total_tasa_ars',
        'lebac8m_total_tasa_ars',
        'lebac9m_total_tasa_ars',
        'lebac10m_total_tasa_ars',
        'lebac11m_total_tasa_ars',
        'lebac12m_total_tasa_ars',
        'lebac18m_total_tasa_ars',
        'lebac24m_total_tasa_ars',
        'cer6m_total_tasa_ars',
        'cer12m_total_tasa_ars',
        'cer18m_total_tasa_ars',
        'cer24m_total_tasa_ars',
        'lebacUSDenARS1m_total_tasa_usd',
        'lebacUSDenARS6m_total_tasa_usd',
        'lebacUSDenARS12m_total_tasa_usd',
        'lebacUSDenUSD1m_total_tasa_usd',
        'lebacUSDenUSD3m_total_tasa_usd',
        'lebacUSDenUSD6m_total_tasa_usd',
        'lebacUSDenUSD12m_total_tasa_usd',
        'nobacBadlar9m_total_tasa_ars',
        'nobacBadlar1y_total_tasa_ars',
        'nobacBadlar2y_total_tasa_ars',
        'nobacBadlar2y_priv_tasa_ars',
        'notaliq190d_total_tasa_ars',
    ]
}