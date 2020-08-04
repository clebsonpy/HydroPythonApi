import pandas as pd

from unittest import TestCase
from .sar import Reservoirs


class TestApi(TestCase):

    # def test_get_data_from_ana_hydro(self):
    #     flow = Flow(station="49330000", source="ANA")
    #     print(flow)
    #     print(flow.station)
    #
    # def test_get_data_from_ana_hydro_list(self):
    #     flow = Flow(station=["49330000", "49370000"], source="ANA")
    #     print(flow)
    #     print(flow.station)

    def test_get_data_from_ana_sar(self):
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

    # def test_get_data_from_ana_sar_list(self):
    #     flow = Flow(station=["19086", "19002"], source="SAR")
    #     print(flow)
    #     print(flow.station)