from hydro_api.ana.sar import Reservoirs
from hydro_api.ana.hidro import Stations, SerieTemporal, EntityApi

# reservoir = Reservoirs()["19086"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)

# station = SerieTemporal(code='00835026', type_data='2')
entity = EntityApi(code_entity='30')
print(entity['30'].name)
