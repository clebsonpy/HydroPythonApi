import pandas as pd
from datetime import datetime
from ..api_biuld import ApiBiuld


class SerieTemporalNis:

    def __init__(self):
        self.volume = pd.DataFrame()
        self.height = pd.DataFrame()
        self.affluence = pd.DataFrame()
        self.flow = pd.DataFrame()


class SerieTemporalNor:

    def __init__(self):
        self.volume = pd.DataFrame()
        self.height = pd.DataFrame()
        self.code_hydro = None
        self.capacity = None


class SerieTemporal(ApiBiuld):
    url = ["http://sarws.ana.gov.br/SarWebService.asmx/DadosHistoricosSIN",
           "http://sarws.ana.gov.br/SarWebService.asmx/DadosHistoricosReservatorios"]

    params = {'CodigoReservatorio': '', 'DataInicial': '', 'DataFinal': ''}

    def __init__(self, code, date_start='01/01/1900', date_end=datetime.now().date().strftime("%d/%m/%Y"), tag=None):
        kwargs = {'CodigoReservatorio': code, 'DataInicial': date_start, 'DataFinal': date_end}
        self.tag = tag
        super()._get(**kwargs)
        self.params.update(kwargs)
        root = self.requests()
        self.data = self._get(root=root)

    def _get(self, root):
        if self.tag == "{http://sarws.ana.gov.br}ReservatorioSIN":
            series = SerieTemporalNis()
            for i in root[0]:
                try:
                    date = pd.to_datetime(i[6].text.strip())
                    code = i[0].text.strip()
                    series.volume.at[date, code] = float(i[2].text.strip())
                    series.height.at[date, code] = float(i[3].text.strip())
                    series.affluence.at[date, code] = float(i[4].text.strip())
                    series.flow.at[date, code] = float(i[5].text.strip())
                except AttributeError:
                    pass
            return series
        elif self.tag == "{http://sarws.ana.gov.br}ReservatorioNordeste":
            series = SerieTemporalNor()
            for i in root[1]:
                try:
                    date = pd.to_datetime(i[4].text.strip())
                    code = i[0].text.strip()
                    series.code_hydro = i[5].text.strip()
                    series.volume.at[date, code] = float(i[3].text.strip())
                    series.height.at[date, code] = float(i[2].text.strip())
                    series.capacity = float(i[6].text.strip())
                except AttributeError:
                    pass
            return series


