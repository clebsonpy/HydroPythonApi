import json

import pandas as pd

from ..ana.api_build import ApiBuild


class _Station:

    def __init__(self, oscar, code, name, capital, situation, wsi, district, altitude, state,
                 lat, lon, type_station, entity, start_date, end_date):
        self.code = code
        self.oscar = oscar
        self.name = name
        self.capital = capital
        self.end_operation = end_date
        self.situation = situation
        self.wsi = wsi
        self.district = district
        self.latitude = lat
        self.longitude = lon
        self.altitude = altitude
        self.state = state
        # self.city = city
        self.entity = entity
        self.date_start = start_date
        self.type_station = type_station
        self.__series_temporal = None

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nLat: {self.latitude}\nLon: {self.longitude}" \
               f"\nEntidade: {self.entity}"


class Stations(ApiBuild):
    url = f'https://apitempo.inmet.gov.br/estacoes/'
    source = 'INMET'

    def __init__(self, station_type: str):
        """
        :param station_type: 'automatic' or 'conventional'
        :return: self
        """

        if station_type == 'automatic':
            self.url = "".join((self.url, "T/"))

        elif station_type == 'conventional':
            self.url = "".join((self.url, "M/"))

        root = self.requests()
        self.__stations = {}
        self.__df_stations = None
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

    def get_dataframe(self):

        return self.__df_stations

    def _get(self, root):

        self.__df_stations = pd.read_json(json.dumps(root))
        self.__df_stations.set_index('CD_ESTACAO', inplace=True)

        for idx in self.__df_stations.index:

            obj = _Station(code=idx,
                           name=self.__df_stations.loc[idx, 'DC_NOME'],
                           lat=self.__df_stations.loc[idx, 'VL_LATITUDE'],
                           lon=self.__df_stations.loc[idx, 'VL_LONGITUDE'],
                           altitude=self.__df_stations.loc[idx, 'VL_ALTITUDE'],
                           type_station=self.__df_stations.loc[idx, 'TP_ESTACAO'],
                           entity=self.__df_stations.loc[idx, 'SG_ENTIDADE'],
                           oscar=self.__df_stations.loc[idx, 'CD_OSCAR'],
                           start_date=self.__df_stations.loc[idx, 'DT_INICIO_OPERACAO'],
                           state=self.__df_stations.loc[idx, 'SG_ESTADO'],
                           capital=self.__df_stations.loc[idx, 'FL_CAPITAL'],
                           end_date=self.__df_stations.loc[idx, 'DT_FIM_OPERACAO'],
                           district=self.__df_stations.loc[idx, 'CD_DISTRITO'],
                           situation=self.__df_stations.loc[idx, 'CD_SITUACAO'],
                           wsi=self.__df_stations.loc[idx, 'CD_WSI'])

            self.__stations[obj.code] = obj
