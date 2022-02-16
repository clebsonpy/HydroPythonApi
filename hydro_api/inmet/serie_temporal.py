import json
import pandas as pd
from ..ana.api_build import ApiBuild


class SerieTemporal(ApiBuild):
    url = "https://apitempo.inmet.gov.br/estacao/"
    source = 'INMET'

    def __init__(self, code: str, aggregation: str, start_date: str,
                 end_date: str = pd.to_datetime("today").strftime("%Y-%m-%d"), tz: str = None):
        """
            Series Temporal
            :param code: Code of the station as a string
            :param aggregation: daily or hour
            :param start_date: Start date (YYYY-MM-DD)
            :param end_date: End Date (YYYY-MM-DD)
            :return: pd.DataFrame(
                index='Date',
                columns=['code', ''])
        """

        if aggregation == 'daily':
            self.url = ''.join((self.url, 'diaria', '/', start_date, '/', end_date, '/', code, '/'))

        elif aggregation == 'hour':
            self.url = ''.join((self.url, start_date, '/', end_date, '/', code, '/'))

        else:
            raise TypeError

        root = self.requests()
        self.data = self._get(root=root, tz=tz)

    def _get(self, root, tz):
        return pd.read_json(json.dumps(root))
    #
    #     series = []
    #     for month in root.iter('SerieHistorica'):
    #         flow = []
    #         code = month.find('EstacaoCodigo').text
    #         date_str = month.find('DataHora').text
    #         if tz is None:
    #             date = pd.to_datetime(date_str, dayfirst=True)
    #         else:
    #             date = pd.to_datetime(date_str, dayfirst=True).tz_localize(pytz.timezone(tz))
    #         days = ca.monthrange(date.year, date.month)[1]
    #         consistence = month.find('NivelConsistencia').text
    #         if date.day == 1:
    #             n_days = days
    #         else:
    #             n_days = days - date.day
    #         date_idx = self.__multIndex(date, n_days, consistence)
    #         for i in range(1, n_days+1):
    #             value = self.typesData[self.params['tipoDados']][0].format(i)
    #             try:
    #                 flow.append(float(month.find(value).text))
    #             except TypeError:
    #                 flow.append(month.find(value).text)
    #             except AttributeError:
    #                 flow.append(None)
    #         series.append(pd.Series(flow, index=date_idx, name=code.zfill(8), dtype='float64'))
    #     try:
    #         data_flow = pd.DataFrame(pd.concat(series))
    #     except ValueError:
    #         data_flow = pd.DataFrame(pd.Series(name=self.params['codEstacao'].zfill(8), dtype='float64'))
    #     return data_flow