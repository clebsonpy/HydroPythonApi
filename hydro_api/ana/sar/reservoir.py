import pandas as pd
from ..api_biuld import ApiBiuld
from .serie_temporal import SerieTemporal


class Reservoir:

    def __init__(self, code, name, city, state, tag):
        self.code = code
        self.name = name
        self.city = city
        self.state = state
        self.tag = tag
        self.__series_temporal = None

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nCity: {self.city}\nState: {self.state}\ntag: {self.tag}"

    @property
    def series_temporal(self):
        if self.__series_temporal is None:
            self.__series_temporal = SerieTemporal().get(code=self.code, tag=self.tag)
        return self.__series_temporal


class Reservoirs(ApiBiuld):
    url = ["http://sarws.ana.gov.br/SarWebService.asmx/ReservatoriosSIN",
           "http://sarws.ana.gov.br/SarWebService.asmx/ReservatoriosNordeste"]
    params = {}

    def __init__(self):
        self._reservoirs = self.get()
        self.__reservoir = {}

    def __str__(self):
        return self._reservoirs.__str__()

    def __getitem__(self, item):
        if item in self.__reservoir:
            return self.__reservoir[item]
        return self.get(code=item)

    def get_reservoirs(self):
        return self._reservoirs

    def get(self, code=None):
        if code is not None:
            reservoir = self._reservoirs.loc[self._reservoirs["Code"] == code]
            reser = Reservoir(code=reservoir["Code"].values[0], name=reservoir["Name"].values[0],
                              city=reservoir["City"].values[0], state=reservoir["State"].values[0],
                              tag=reservoir["tag"].values[0])

            self.__reservoir[code] = reser
            return reser

        root = self.requests()

        reservoir = {"Code": [], "Name": [], "City": [], "State": [], "tag": []}

        for i in root:
            for j in i:
                reservoir["Code"].append(f"{j[0].text.strip()}")
                reservoir["Name"].append(f"{j[1].text.strip()}")
                reservoir["City"].append(f"{j[2].text.strip()}")
                reservoir["State"].append(f"{j[3].text.strip()}")
                reservoir["tag"].append(f"{j.tag}")

        return pd.DataFrame(reservoir)
