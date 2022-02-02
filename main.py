
import timeit
# from hydro_api.ana.sar import Reservoirs
from hydro_api.inmet import Stations
# from hydro_api.ana.telemetric import Stations, SerieTemporal

# reservoir = Reservoirs()["19086"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)

# station = SerieTemporal(code='00835026', type_data='2')
ini = timeit.default_timer()
# stations = SerieTemporal(code='39580000', start_date='20/12/2021', end_date='')
# print(stations.data)

stations = Stations(station_type='conventional')
print(stations.get_dataframe())
print(stations['A422'])
print(stations.stations_code)

# print(stations['39580000'])
# alagoas = stations.get_stations(state='AL')
# print(alagoas)
# print(dataframe['City'].apply(split('-'), axis=1))
fim = timeit.default_timer()

print('Duracao: ', fim - ini)
