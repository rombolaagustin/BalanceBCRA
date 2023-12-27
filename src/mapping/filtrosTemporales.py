from datetime import datetime

MONTHS = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo',
    6: 'junio',
    7: 'julio',
    8: 'agosto',
    9: 'septiembre',
    10: 'octubre',
    11: 'noviembre',
    12: 'diciembre',
}

FILTROS_TEMPORALES = {
    'Personalizada': 'custom',
    'Presidencia Javier Milei': 'presidency_milei',
    'Presidencia Alberto Fernandez': 'presidency_af',
    'Presidencia Mauricio Macri': 'presidency_macri',
    'Presidencia Cristina Fernandez (II)': 'presidency_cfk2',
    'Presidencia Cristina Fernandez (I)': 'presidency_cfk1',
    'Presidencia Nestor Kirchner': 'presidency_nk',
    'Ministro Economía: Sergio Massa': 'mecon_massa',
    'Ministro Economía: Silvina Batakis': 'mecon_batakis',
    'Ministro Economía: Martín Guzmán': 'mecon_guzman',
}

FECHAS_ESPECIALES = {
    'presidency_milei': {
        'start': datetime(year=2023, month=12, day=10),
        'end': datetime(year=2027, month=12, day=10),
    },
    'presidency_af': {
        'start': datetime(year=2019, month=12, day=10),
        'end': datetime(year=2023, month=12, day=10),
    },
    'presidency_macri': {
        'start': datetime(year=2015, month=12, day=10),
        'end': datetime(year=2019, month=12, day=10),
    },
    'presidency_cfk2': {
        'start': datetime(year=2011, month=12, day=10),
        'end': datetime(year=2015, month=12, day=10),
    },
    'presidency_cfk1': {
        'start': datetime(year=2007, month=12, day=10),
        'end': datetime(year=2011, month=12, day=10),
    },
    'presidency_nk': {
        'start': datetime(year=2003, month=5, day=25),
        'end': datetime(year=2007, month=12, day=10),
    },
    'mecon_massa': {
        'start': datetime(year=2022, month=7, day=28),
        'end': datetime(year=2023, month=12, day=10),
    },
    'mecon_batakis': {
        'start': datetime(year=2022, month=7, day=4),
        'end': datetime(year=2022, month=7, day=28),
    },
    'mecon_guzman': {
        'start': datetime(year=2019, month=12, day=10),
        'end': datetime(year=2022, month=7, day=4),
    },
}

# VARIACIONES TEMPORALES

VARIACIONES = {
    'Anual': 365,
    'Mensual': 30,
    'Semanal': 7,
    'Personalizado': None,
}
