from datetime import datetime

FILTROS_TEMPORALES = {
    'Personalizada': 'custom',
    'Presidencia Alberto Fernandez': 'presidency_af',
    'Presidencia Mauricio Macri': 'presidency_macri',
    'Presidencia Cristina Fernandez (II)': 'presidency_cfk2',
    'Presidencia Cristina Fernandez (I)': 'presidency_cfk1',
    'Presidencia Nestor Kirchner': 'presidency_nk',
}

FECHAS_ESPECIALES = {
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
}