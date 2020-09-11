import pandas as pd
from ..api_biuld import ApiBiuld


class _Watersheds:

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}"

    def __repr__(self):
        return self.name


class _Basin:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self._watersheds = {}

    @property
    def watersheds(self):
        return self._watersheds

    @watersheds.setter
    def watersheds(self, watersheds):
        self._watersheds[watersheds.code] = watersheds

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}"


class BasinApi(ApiBiuld):

    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroBaciaSubBacia'
    params = {'codBacia': '', 'codSubBacia': ''}

    def __init__(self,  code_basin='', code_watersheds=''):
        kwargs = {'codBacia': code_basin, 'codSubBacia': code_watersheds}
        super()._get(**kwargs)

        self.params.update(kwargs)
        self.basins = pd.DataFrame(columns=['Name'])
        self.subbasins = pd.DataFrame(columns=['Name'])
        self.__watersheds = {}
        self.__basin = {}
        root = self.requests()
        self._get(root)

    def __getitem__(self, item):
        return self.__basin[item]

    def watersheds(self, code):
        return self.subbasins.loc[code]

    def _get(self, root):

        basin_code = None
        for basin in root.iter('Table'):
            code_basin = basin.find('codBacia').text
            self.basins.at[code_basin, 'Name'] = basin.find('nmBacia').text
            code_subbasin = basin.find('codSubBacia').text
            self.subbasins.at[code_subbasin, 'Name'] = basin.find('nmSubBacia').text
            if basin_code == code_basin:
                for i in self.subbasins.index:
                    self.__watersheds[i] = _Watersheds(name=self.subbasins["Name"][i], code=i)

                    self.__basin[code_basin].watersheds = self.__watersheds[i]
            else:
                self.__basin[self.basins.index.values[0]] = _Basin(name=self.basins["Name"].values[0],
                                                                   code=self.basins.index.values[0])
                basin_code = code_basin
