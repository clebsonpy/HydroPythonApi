from hydro_api.ana.sar.reservoir import Reservoirs
from hydro_api.ana.sar.serie_temporal import SerieTemporal

reservoir = Reservoirs()
serie = SerieTemporal()

print(serie.get(code="12541", date_start="03/04/2019").volume)
print(reservoir)

