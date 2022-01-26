from datetime import datetime, timezone

import pytz

import pandas as pd
import numpy as np
import calendar as ca

from hydro_api.ana.hidro import serie_temporal
from ..api_biuld import ApiBiuld


class SerieTemporal(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos'
    params = {'codEstacao': '', 'dataInicio': '', 'dataFim': ''}

    def __init__(self, code: str, start_date: str = '', end_date: str = '', tz: str = None):
        """
            :param code:
            :param date_start:
            :param date_end:
            :return: pd.DataFrame(index='Date, Consistence', columns=['Code'])
        """
        kwargs = {'codEstacao': code, 'dataInicio': start_date, 'dataFim': end_date}

        super()._get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()
        self.data = self._get(root=root, tz=tz)

    def _get_text(self, element):
        try:
            value = element.text
            return value if value else np.NaN
        
        except AttributeError:
            return np.NaN

    def _get(self, root, tz):

        dataframe = pd.DataFrame(columns=['rainfall', 'height', 'flow'])
        for data in root.iter('DadosHidrometereologicos'):

            date_str = self._get_text(element=data.find('DataHora'))
            if date_str:
                if tz is None:
                    date = pd.to_datetime(date_str, dayfirst=True)
                else:
                    date = pd.to_datetime(date_str, dayfirst=True).tz_localize(pytz.timezone(tz))
                
                dataframe.at[date, 'rainfall'] = float(self._get_text(element=data.find('Chuva')))
                dataframe.at[date, 'height'] = float(self._get_text(element=data.find('Nivel')))
                dataframe.at[date, 'flow'] = float(self._get_text(element=data.find('Vazao')))

        return dataframe
