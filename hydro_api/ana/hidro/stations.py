import pandas as pd

from ..api_biuld import ApiBiuld
from ..hidro.basin import BasinApi
from ..hidro.serie_temporal import SerieTemporal


class _Station:

    def __init__(self, code, name, lat, lon, city, type_station, watersheds, responsible, operator, area):
        self.code = code
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.city = city
        self.watersheds = BasinApi(code_watersheds=watersheds).watersheds(code=watersheds)
        self.responsible = responsible
        self.operator = operator
        self.area = area
        self.type_station = type_station
        self.__series_temporal = None

    def series_temporal(self, type_data: str = None):
        if self.type_station == "1":
            if type_data == "3":
                self.__series_temporal = SerieTemporal(code=self.code, type_data='3').data
            elif type_data == "1":
                self.__series_temporal = SerieTemporal(code=self.code, type_data='1').data
        elif self.type_station == "2":
            self.__series_temporal = SerieTemporal(code=self.code, type_data='2').data
        return self.__series_temporal

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nLat: {self.latitude}\nLon: {self.longitude}" \
               f"\nResponsible: {self.responsible}\nOperator: {self.operator}\nWatersheds: {self.watersheds.name}"


class Stations(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario'
    params = {'codEstDE': '', 'codEstATE': '', 'tpEst': '', 'nmEst': '', 'nmRio': '', 'codSubBacia': '', 'codBacia': '',
              'nmMunicipio': '', 'nmEstado': '', 'sgResp': '', 'sgOper': '', 'telemetrica': ''}

    def __init__(self, code_start: str = '', code_end: str = '', type_station: str = '', name: str = '',
                 name_river: str = '', code_watersheds: str = '', code_basin: str = '', name_city: str = '',
                 name_state: str = '', responsible: str = '', operator: str = '', telemetrica: str = ''):
        """
        :param code_start: Código de 8 dígitos da estação - INICIAL (Ex.: 00047000)
        :param code_end: Código de 8 dígitos da estação - FINAL (Ex.: 90300000)
        :param type_station: Tipo da estação (1-Flu ou 2-Plu)
        :param name: Nome da Estação (Ex.: Barra Mansa)
        :param name_river: Nome do Rio (Ex.: Rio Javari)
        :param code_watersheds: Código da Sub-Bacia hidrografica (Ex.: 10)
        :param code_basin: Código da Bacia hidrografica (Ex.: 1)
        :param name_city: Município (Ex.: Itaperuna)
        :param name_state: Estado (Ex.: Rio de Janeiro)
        :param responsible: Sigla do Responsável pela estação (Ex.: ANA)
        :param operator: Sigla da Operadora da estação (Ex.: CPRM)
        :param telemetrica: (Ex: 1-SIM ou 0-NÃO)
        :return: self
        """

        kwargs = {'codEstDE': code_start, 'codEstATE': code_end, 'tpEst': type_station, 'nmEst': name,
                  'nmRio': name_river, 'codSubBacia': code_watersheds, 'codBacia': code_basin, 'nmMunicipio': name_city,
                  'nmEstado': name_state, 'sgResp': responsible, 'sgOper': operator,
                  'telemetrica': ''}

        super()._get(**kwargs)
        self.params.update(kwargs)
        root = self.requests()

        self.__stations = {}
        self.__df_stations = pd.DataFrame(columns=[
            'Name', 'Latitude', 'Longitude', 'Watersheds', 'Type', 'City', 'Responsible', 'Operator', 'Area'])
        self._get(root)

    def __str__(self):
        return self.__df_stations.__str__()

    def __getitem__(self, item) -> _Station:
        """
        :param item: Código de 8 dígitos da estação - INICIAL (Ex.: 00047000)
        :return:
        """
        if item in self.__stations:
            return self.__stations[item]

    def _get(self, root):
        for i in root.iter():
            print(i)

        for station in root.iter('Table'):
            print(station)
            code = station.find('Codigo').text
            self.__df_stations.at[code, 'Name'] = station.find('Nome').text
            self.__df_stations.at[code, 'Latitude'] = station.find('Latitude').text
            self.__df_stations.at[code, 'Longitude'] = station.find('Longitude').text
            self.__df_stations.at[code, 'Watersheds'] = station.find('SubBaciaCodigo').text
            self.__df_stations.at[code, 'Type'] = station.find('TipoEstacao').text
            self.__df_stations.at[code, 'City'] = station.find('MunicipioCodigo').text
            self.__df_stations.at[code, 'Responsible'] = station.find('ResponsavelCodigo').text
            self.__df_stations.at[code, 'Operator'] = station.find('OperadoraCodigo').text
            self.__df_stations.at[code, 'Area'] = station.find('AreaDrenagem').text

            obj = _Station(code=code, name=station.find('Nome').text, lat=station.find('Latitude').text,
                           lon=station.find('Longitude').text, watersheds=station.find('SubBaciaCodigo').text,
                           type_station=station.find('TipoEstacao').text, city=station.find('MunicipioCodigo').text,
                           responsible=station.find('ResponsavelCodigo').text,
                           operator=station.find('OperadoraCodigo').text, area=station.find('AreaDrenagem').text)
            self.__stations[obj.code] = obj
