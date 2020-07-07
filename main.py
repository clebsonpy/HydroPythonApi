from hydro_api.ana.sar.reservoir import Reservoirs
from hydro_api.ana.sar.serie_temporal import SerieTemporal
from hydro_api.ana.hidro.inventory import Inventory
from hydro_api.ana.hidro.basin import BasinApi

station = Inventory()["49330000"]
print(station.series_temporal["Flow"])
print(station.series_temporal["Height"])


reservoir = Reservoirs()
serie = SerieTemporal()

print(serie.get(code="12541", date_start="03/04/2019").volume)
print(reservoir)

