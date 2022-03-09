
import timeit
from hydro_api.inmet import Stations, SerieTemporal
# from hydro_api.ana.telemetric import Stations, SerieTemporal


ini = timeit.default_timer()
stations = SerieTemporal(code='A756', aggregation='hour', start_date='2021-12-20')
series_temporal = stations.data
print(series_temporal)
for data in series_temporal:
    if data == 'VEN_VEL':
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
