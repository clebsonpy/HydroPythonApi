import pandas as pd
from ..api_biuld import ApiBiuld
from ..hidro.serie_temporal import SerieTemporal
from ..hidro.basin import BasinApi


class _Station:

    def __init__(self, code, name, lat, lon, city, type_station, watersheds, responsible, operator, area):
        self.code = code
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.city = city
        self.watersheds = BasinApi().get(code_watersheds=watersheds).watersheds[watersheds]
        self.responsible = responsible
        self.operator = operator
        self.area = area
        self.type_station = type_station
        self.__series_temporal = None

    def series_temporal(self, type_data=None):
        if self.type_station == "1":
            if type_data == "3":
                self.__series_temporal = SerieTemporal().get(code=self.code, type='3')
            elif type_data == "1":
                self.__series_temporal = SerieTemporal().get(code=self.code, type='1')
        elif self.type_station == "2":
            self.__series_temporal = SerieTemporal().get(code=self.code, type='2')
        return self.__series_temporal

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nLat: {self.latitude}\nLon: {self.longitude}" \
               f"\nResponsible: {self.responsible}\nOperator: {self.operator}\nWatersheds: {self.watersheds.name}"


class Inventory(ApiBiuld):

    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'
    params = {'codEstDE': '', 'codEstATE': '', 'tpEst': '', 'nmEst': '', 'nmRio': '', 'codSubBacia': '', 'codBacia': '',
              'nmMunicipio': '', 'nmEstado': '', 'sgResp': '', 'sgOper': '', 'telemetrica': ''}

    def __init__(self):
        self.__stations = {}

    def __getitem__(self, item):
        if item in self.__stations:
            return self.__stations[item]
        return self.get(code_start=item)

    def get(self, code_start='', code_end='', type='', name='', name_river='', code_watersheds='', code_basin='',
            name_city='', name_state='', responsible='', operator='', telemetrica=''):
        """
        :param code_start: Código de 8 dígitos da estação - INICIAL (Ex.: 00047000)
        :param code_end: Código de 8 dígitos da estação - FINAL (Ex.: 90300000)
        :param type: Tipo da estação (1-Flu ou 2-Plu)
        :param name: Nome da Estação (Ex.: Barra Mansa)
        :param name_river: Nome do Rio (Ex.: Rio Javari)
        :param code_watersheds: Código da Sub-Bacia hidrografica (Ex.: 10)
        :param code_basin: Código da Bacia hidrografica (Ex.: 1)
        :param name_city: Município (Ex.: Itaperuna)
        :param name_state: Estado (Ex.: Rio de Janeiro)
        :param responsible: Sigla do Responsável pela estação (Ex.: ANA)
        :param operator: Sigla da Operadora da estação (Ex.: CPRM)
        :param telemetrica: (Ex: 1-SIM ou 0-NÃO)
        :return: pd.DataFrame
        """
        kwargs = {'codEstDE': code_start, 'codEstATE': code_end, 'tpEst': type, 'nmEst': name, 'nmRio': name_river,
                  'codSubBacia': code_watersheds, 'codBacia': code_basin, 'nmMunicipio': name_city,
                  'nmEstado': name_state, 'sgResp': responsible, 'sgOper': operator, 'telemetrica': telemetrica}

        super().get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()

        stations = pd.DataFrame(columns=[
            'Name', 'Latitude', 'Longitude', 'Watersheds', 'Type', 'City', 'Responsible', 'Operator', 'Area'
        ])
        for station in root.iter('Table'):
            code = station.find('Codigo').text
            stations.at[code, 'Name'] = station.find('Nome').text
            stations.at[code, 'Latitude'] = station.find('Latitude').text
            stations.at[code, 'Longitude'] = station.find('Longitude').text
            stations.at[code, 'Watersheds'] = station.find('SubBaciaCodigo').text
            stations.at[code, 'Type'] = station.find('TipoEstacao').text
            stations.at[code, 'City'] = station.find('MunicipioCodigo').text
            stations.at[code, 'Responsible'] = station.find('ResponsavelCodigo').text
            stations.at[code, 'Operator'] = station.find('OperadoraCodigo').text
            stations.at[code, 'Area'] = station.find('AreaDrenagem').text
        if len(stations) == 1:
            station = _Station(code=stations.index.values[0], name=stations['Name'].values[0],
                               lat=stations["Latitude"].values[0], lon=stations["Longitude"].values[0],
                               watersheds=stations["Watersheds"].values[0], type_station=stations["Type"].values[0],
                               city=stations["City"].values[0], responsible=stations["Responsible"].values[0],
                               operator=stations["Operator"].values[0], area=stations["Area"].values[0])
            return station
        return stations
