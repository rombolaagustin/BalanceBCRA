import pandas as pd
import warnings

from .mapping.mapBalanceBCRA import COLUMNS_NAMES
from .mapping.mapBalanceBCRA import SHEET_NAMES

# Desactivar temporalmente todas las advertencias de pandas
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

class descriptObj():
    def __init__(self):
        aux = list()
        for sheet_name, data_name in SHEET_NAMES.items():
            for colName in COLUMNS_NAMES[sheet_name]:
                if not('date' in colName) and not('delete' in colName) and not('tipoSerie' in colName):
                    aux.append({
                        'sheet': data_name,
                        'name': colName.split('_')[0],
                        'sector': colName.split('_')[1],
                        'tipo': colName.split('_')[2],
                        'currency': colName.split('_')[3],
                        'realName': colName,
                        'fullName': f"{data_name}_{colName}",
                        })
        self.df = pd.DataFrame(aux)

    def getFullNameFromName(self, name: list) -> list:
        fullName = self.df[self.df['name'].isin(name)]['fullName'].values
        return fullName

    def getFullNameFromRealName(self, realName: list) -> list:
        fullName = self.df[self.df['realName'].isin(realName)]['fullName'].values
        return fullName 

    def getDataFromFullName(self, fullName: str) -> dict:
        info = self.df[self.df['fullName']==fullName].to_dict()
        return info

    def getColumnsByCurrency(self, currency: str) -> list:
        cols = self.df[self.df['currency']==currency]['fullName'].values
        return cols

    def getColumnsByTipo(self, tipo: str) -> list:
        cols = self.df[self.df['tipo']==tipo]['fullName'].values
        return cols

    def getColumnsFull(self, 
        sheet:str,
        tipos: list):
        cols = self.df[
            (self.df['sheet']==sheet) &
            (self.df['tipo'].isin(tipos))]['realName'].values
        return cols


class dataContent():

    def __setDescript(self):
        self.descript = descriptObj()
        
    def __init__(self, filename: str, filename_cer: str = ''):
        # Se inicializan los atributos ocultos
        self.__data_raw = dict()
        self.__filename = filename
        self.__setDescript()
        for sheet_name, data_name in SHEET_NAMES.items():
            print(f'Procesando {sheet_name} --> {data_name}')
            self.__data_raw[data_name] = pd.read_excel(
                engine='openpyxl',
                io=filename,
                sheet_name=sheet_name,
                header=None,
                skiprows=9,
                names=COLUMNS_NAMES[sheet_name]
                )

            # Se filtran los datos diarios   
            if 'tipoSerie' in self.__data_raw[data_name].columns:
                self.__data_raw[data_name] = self.__data_raw[data_name][self.__data_raw[data_name]['tipoSerie']=='D']
            for col_name in COLUMNS_NAMES[sheet_name]:
                if 'delete' in col_name or 'tipoSerie' in col_name:
                    self.__data_raw[data_name] = self.__data_raw[data_name].drop(col_name, axis=1)
                elif 'date' == col_name:
                    pass
                else:
                    self.__data_raw[data_name][col_name] = pd.to_numeric(self.__data_raw[data_name][col_name].replace(',', '', regex=True), errors='coerce')
                    if pd.isna(self.__data_raw[data_name][col_name].iloc[0]):
                        # replace the first NaN value with 0
                        self.__data_raw[data_name][col_name].iloc[0] = 0
                    self.__data_raw[data_name][col_name] = self.__data_raw[data_name][col_name].fillna(method='ffill')

            # Filling data
            self.__data_raw[data_name].index = self.__data_raw[data_name]['date']
            del self.__data_raw[data_name]['date']

            # STOCKS
            # Se toma la baseMonetaria como la base para mergear            
            if data_name == 'baseMonetaria':
                usefulCols = self.descript.getColumnsFull(data_name, ['stock', 'indice'])
                self.stocks = self.__data_raw['baseMonetaria'][usefulCols].resample('1D').interpolate(method='linear')
            else:
                usefulCols = self.descript.getColumnsFull(data_name, ['stock', 'indice'])
                self.stocks = self.stocks.merge(self.__data_raw[data_name][usefulCols].resample('1D').interpolate(), left_index=True, right_index=True, how='left')
        
        
        # Rename columns in stocks
        rename_cols = {c: self.descript.getFullNameFromRealName([c])[0] for c in self.stocks.columns}
        print(rename_cols)
        self.stocks = self.stocks.rename(columns=rename_cols)
        self.stocks = self.stocks.round(2)
        
        # Agrega el CER
        if len(filename_cer) > 0:
            df_cer = pd.read_excel(
                    engine='xlrd',
                    io='data/diar_cer.xls',
                    header=1,
                    skiprows=25,
                    )    
            df_cer['cd_serie'] = pd.to_datetime(df_cer['cd_serie'], format='%d/%m/%Y')
            df_cer.index = df_cer['cd_serie']
            df_cer = df_cer.rename(columns={3540: 'indices_CER_total_indice_ars', 'cd_serie': 'date'})
            del df_cer['date']
            print(df_cer.columns)
            self.stocks = self.stocks.merge(df_cer, left_index=True, right_index=True, how='left')


    def getRangeDate(self):
        return self.stocks.index.min().date(), self.stocks.index.max().date()

    def getStocks(
        self, 
        where:list, 
        sector:list, 
        tipo:list, 
        currency:list,
        filtro_fecha=dict(),
        base_100=False,
        ):
        listColumns = list()
        for col in self.stocks.columns:
            r = col.split('_')
            if r[0] in where and r[2] in sector and r[3] in tipo and r[4] in currency:
                listColumns.append(col)
        df = self.stocks[listColumns]
        if 'start' in filtro_fecha and 'end' in filtro_fecha:
            df = df[(df.index >= filtro_fecha['start']) & (df.index <= filtro_fecha['end'])]
        if base_100:
            for col in df.columns:
                df[col] = 100*(df[col]/df[col].values[0])
        return df