
import timeit
# from hydro_api.ana.sar import Reservoirs
# from hydro_api.inmet import Stations, SerieTemporal
from hydro_api.ana.telemetric import Stations, SerieTemporal

# reservoir = Reservoirs()["19086"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)

# station = SerieTemporal(code='00835026', type_data='2')
ini = timeit.default_timer()
stations = SerieTemporal(code='39580000', start_date='20/12/2021', end_date='')
series_temporal = stations.data
print(series_temporal)
for data in series_temporal:
    if data == 'flow':
        series = series_temporal[data]
        for i in series.index:
            print(i)
            series[i]

# stations = Stations(station_type='conventional')
# print(stations.get_dataframe())
# print(stations['A422'])
# print(stations.stations_code)
# series = SerieTemporal('A756', start_date='2022-01-01', aggregation='hour')
# print(series.data.columns)

# print(stations['39580000'])
# alagoas = stations.get_stations(state='AL')
# print(alagoas)
# print(dataframe['City'].apply(split('-'), axis=1))
fim = timeit.default_timer()

print('Duracao: ', fim - ini)
