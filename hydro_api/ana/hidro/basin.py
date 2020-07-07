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

    def get(self, code_basin='', code_watersheds=''):
        kwargs = {'codBacia': code_basin, 'codSubBacia': code_watersheds}

        super().get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()

        basins = pd.DataFrame(columns=['Name'])
        subbasins = pd.DataFrame(columns=['Name'])

        for basin in root.iter('Table'):
            code_basin = basin.find('codBacia').text
            basins.at[code_basin, 'Name'] = basin.find('nmBacia').text
            code_subbasin = basin.find('codSubBacia').text
            subbasins.at[code_subbasin, 'Name'] = basin.find('nmSubBacia').text

        if len(basins) == 1:
            basin = _Basin(name=basins["Name"].values[0], code=basins.index.values[0])
            for i in subbasins.index:
                watersheds = _Watersheds(name=subbasins["Name"][i], code=i)
                basin.watersheds = watersheds
            return basin
        return basins, subbasins