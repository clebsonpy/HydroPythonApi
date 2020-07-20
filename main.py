from hydro_api.ana.sar import Reservoirs
from hydro_api.ana.hidro import Inventory


# reservoir = Reservoirs()["19086"]
inventory = Inventory()["49330000"]
# print(reservoir.series_temporal.flow.to_csv("sar_manso.csv"))
# print(serie.get(code="12541", date_start="03/04/2019").volume)
# print(reservoir.series_temporal.flow)
# print(reservoir.series_temporal.affluence)
print(inventory)
print(inventory.series_temporal(type_data="3"))
