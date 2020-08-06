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
            self.__series_temporal = SerieTemporal(code=self.code, tag=self.tag).data
        return self.__series_temporal


class Reservoirs(ApiBiuld):
    url = ["http://sarws.ana.gov.br/SarWebService.asmx/ReservatoriosSIN",
           "http://sarws.ana.gov.br/SarWebService.asmx/ReservatoriosNordeste"]
    params = {}

    def __init__(self, code=None):
        self.__df_reservoir = pd.DataFrame(columns=["Code", "Name", "City", "State", "tag"])
        self.__reservoir = {}
        root = self.requests()
        self._get(root=root)

    def __str__(self):
        return self.__df_reservoir.__str__()

    def __getitem__(self, item):
        return self.__reservoir[item]

    def _get(self, root):

        for i in root:
            for j in i:
                code = f"{j[0].text.strip()}"
                self.__df_reservoir.at[code, "Name"] = f"{j[1].text.strip()}"
                self.__df_reservoir.at[code, "City"] = f"{j[2].text.strip()}"
                self.__df_reservoir.at[code, "State"] = f"{j[3].text.strip()}"
                self.__df_reservoir.at[code, "tag"] = f"{j.tag}"

                reservoir = Reservoir(code=f"{j[0].text.strip()}", name=f"{j[1].text.strip()}", tag=f"{j.tag}",
                                      city=f"{j[2].text.strip()}", state=f"{j[3].text.strip()}")

                self.__reservoir[reservoir.code] = reservoir
