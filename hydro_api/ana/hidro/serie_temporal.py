import pandas as pd
import calendar as ca
from ..api_biuld import ApiBiuld


class SerieTemporal(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica'
    params = {'codEstacao': '', 'dataInicio': '', 'dataFim': '', 'tipoDados': '', 'nivelConsistencia': ''}
    typesData = {'3': ['Vazao{:02}'], '2': ['Chuva{:02}'], '1': ['Cota{:02}']}

    def __init__(self, code: str, type_data: str, date_start: str = '', date_end: str = '', consistence: str = ''):
        """
            :param code:
            :param type_data: '3' - Flow; '2' - Rainfall; '1' - Height
            :param date_start:
            :param date_end:
            :return: pd.DataFrame(index='Date, Consistence', columns=['Code'])
        """
        kwargs = {'codEstacao': code, 'dataInicio': date_start, 'dataFim': date_end, 'tipoDados': type_data,
                  'nivelConsistencia': consistence}

        super()._get(**kwargs)

        self.params.update(kwargs)
        root = self.requests()
        self.data = self._get(root=root)

    def __multIndex(self, date, n_days, consistence):
        list_date = pd.date_range(date, periods=n_days, freq="D")
        list_cons = [int(consistence)] * n_days
        index_multi = list(zip(*[list_date, list_cons]))
        return pd.MultiIndex.from_tuples(index_multi, names=["Date", "Consistence"])

    def _get(self, root):

        series = []
        for month in root.iter('SerieHistorica'):
            flow = []
            code = month.find('EstacaoCodigo').text
            date_str = month.find('DataHora').text
            date = pd.to_datetime(date_str, dayfirst=True)
            days = ca.monthrange(date.year, date.month)[1]
            consistence = month.find('NivelConsistencia').text
            if date.day == 1:
                n_days = days
            else:
                n_days = days - date.day
            date_idx = self.__multIndex(date, n_days, consistence)
            for i in range(1, n_days+1):
                value = self.typesData[self.params['tipoDados']][0].format(i)
                try:
                    flow.append(float(month.find(value).text))
                except TypeError:
                    flow.append(month.find(value).text)
                except AttributeError:
                    flow.append(None)
            series.append(pd.Series(flow, index=date_idx, name=code.zfill(8), dtype='float64'))
        try:
            data_flow = pd.DataFrame(pd.concat(series))
        except ValueError:
            data_flow = pd.DataFrame(pd.Series(name=self.params['codEstacao'].zfill(8), dtype='float64'))
        return data_flow
