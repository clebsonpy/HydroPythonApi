from re import S
from turtle import st
import pandas as pd

from ..api_biuld import ApiBiuld


class _Station:

    def __init__(self, code, name, lat, lon, alt, city, watersheds, catchment, status, responsible, operator, origin, river):
        self.code = code
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        self.city = city
        self.watersheds = watersheds
        self.catchment = catchment
        self.status = status
        self.responsible = responsible
        self.operator = operator
        self.origin = origin
        self.river = river

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nLat: {self.latitude}\nLon: {self.longitude}" \
               f"\nResponsible: {self.responsible}\nOperator: {self.operator}\nWatersheds: {self.watersheds}"


class Stations(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/ListaEstacoesTelemetricas'
    params = {'statusEstacoes': '', 'origem': ''}

    def __init__(self, status: str = '', origin: str = ''):
        """
        :param statusEstacoes: 0-Ativo ou 1-Manutenção
        :param origem: 0-Todas, 1-ANA/INPE, 2-ANA/SIVAM, 3-RES_CONJ_03, 4-CotaOnline, 5-Projetos Especiais
        """

        kwargs = {'statusEstacoes': status, 'origem': origin}

        super()._get(**kwargs)
        self.params.update(kwargs)
        root = self.requests()

        self.__stations = {}
        self.__df_stations = pd.DataFrame(columns=[
            'Name', 'Latitude', 'Longitude', 'Altitude', 'Watersheds', 'Catchment', 'Status', 'City', 'Responsible', 'Operator', 'Origin', 'River'])
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

    @property
    def stations_code(self):
        return self.__stations.keys()

    def __get_text(self, element):
        try:
            return element.text
        
        except AttributeError:
            return None

    def _get(self, root):

        for station in root.iter('Table'):
            code = station.find('CodEstacao').text
            self.__df_stations.at[code, 'Name'] = self.__get_text(element=station.find('NomeEstacao'))
            self.__df_stations.at[code, 'Latitude'] = self.__get_text(element=station.find('Latitude'))
            self.__df_stations.at[code, 'Longitude'] = self.__get_text(element=station.find('Longitude'))
            self.__df_stations.at[code, 'Altitude'] = self.__get_text(element=station.find('Altitude'))
            self.__df_stations.at[code, 'Watersheds'] = self.__get_text(element=station.find('Bacia'))
            self.__df_stations.at[code, 'Catchment'] = self.__get_text(element=station.find('SubBacia'))
            self.__df_stations.at[code, 'Status'] = self.__get_text(element=station.find('StatusEstacao'))
            self.__df_stations.at[code, 'City'] = self.__get_text(element=station.find('Municipio-UF'))
            self.__df_stations.at[code, 'Responsible'] = self.__get_text(element=station.find('Responsavel'))
            self.__df_stations.at[code, 'Operator'] = self.__get_text(element=station.find('Operadora'))
            self.__df_stations.at[code, 'Origin'] = self.__get_text(element=station.find('Origem'))
            self.__df_stations.at[code, 'River'] = self.__get_text(element=station.find('CodRio'))

            obj = _Station(
                code=code, name=self.__get_text(element=station.find('NomeEstacao')), 
                lat=self.__get_text(element=station.find('Latitude')),
                lon=self.__get_text(element=station.find('Longitude')), 
                alt=self.__get_text(element=station.find('Altitude')), 
                catchment=self.__get_text(element=station.find('SubBacia')), 
                watersheds=self.__get_text(element=station.find('Bacia')),
                status=self.__get_text(element=station.find('StatusEstacao')), 
                city=self.__get_text(element=station.find('Municipio-UF')),
                responsible=self.__get_text(element=station.find('Responsavel')), 
                origin=self.__get_text(element=station.find('Origem')),
                operator=self.__get_text(element=station.find('Operadora')), 
                river=self.__get_text(element=station.find('CodRio')))
            self.__stations[obj.code] = obj
