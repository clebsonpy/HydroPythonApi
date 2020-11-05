from hydro_api.ana.sar import Reservoirs
from hydro_api.ana.hidro import Stations, SerieTemporal

# reservoir = Reservoirs()["19086"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)

station = SerieTemporal(code='39431000', type_data='3')
print(station.data)