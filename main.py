from hydro_api.ana.sar import Reservoirs
# from hydro_api.ana.hidro import Stations, SerieTemporal, EntityApi
from hydro_api.ana.telemetric import Stations, SerieTemporal

# reservoir = Reservoirs()["19086"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)

# station = SerieTemporal(code='00835026', type_data='2')
stations = SerieTemporal(code='1448000', start_date='20/01/2022', end_date='24/01/2022')
print(stations.data)

# stations = Stations()
# print(stations)
