import pandas as pd

from unittest import TestCase
from .sar import Reservoirs
from .hidro import Stations
from .hidro.serie_temporal import SerieTemporal


class TestApi(TestCase):

    def test_get_stations_by_city(self):
        recife = Stations(name_city="RECIFE")
        piranhas = Stations(name_city="PIRANHAS")
        print(recife["39098600"])
        print(piranhas["49330000"])

    def test_get_data_from_ana_hydro_serie_temporal(self):
        serie = SerieTemporal(code="01036007", type_data='2')
        print(serie.data)

    def test_get_data_from_ana_hydro_flow_height_none(self):
        stations = Stations(code_start="49330000")
        stations_xingo = stations
        print(stations_xingo["49330000"])

    def test_get_data_from_ana_hydro_flow_height(self):
        stations = Stations(code_start="49330000")
        stations_xingo = stations
        print(stations_xingo["49330000"].series_temporal(type_data='3'))
        print(stations_xingo["49330000"].series_temporal(type_data='1'))

    def test_get_from_ana_hydro_rainfall(self):
        stations = Stations(name_city="RECIFE")
        stations_recife = stations
        print(stations_recife["834003"].type_station)
        print(stations_recife["834003"].series_temporal(type_data='2'))

    def test_get_data_from_sar(self):
        reservoir = Reservoirs()["19086"]
        aflue = reservoir.series_temporal.affluence
        deflu = reservoir.series_temporal.flow
        afluencia = [192.00, -68301.00, 68795.00, 382.00, 489.00, 719.00]
        defluencia = [78.00, 122.00, 95.00, 105.00, 173.00, 245.00]
        data_flow = {"A19086": afluencia, "D19086": defluencia}
        data = ["05/01/2002", "06/01/2002", "07/01/2002", "08/01/2002", "09/01/2002", "10/01/2002"]
        data = pd.to_datetime(data, dayfirst=True)
        data_obs = pd.DataFrame(index=data, data=data_flow)
        for i in data_obs.index:
            self.assertEqual(data_obs["D19086"][i], deflu["19086"][i])
            self.assertEqual(data_obs["A19086"][i], aflue["19086"][i])
