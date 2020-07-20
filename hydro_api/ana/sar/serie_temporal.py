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

    def get(self, code, date_start='01/01/1900', date_end=datetime.now().date().strftime("%d/%m/%Y"), tag=None):
        kwargs = {'CodigoReservatorio': code, 'DataInicial': date_start, 'DataFinal': date_end}

        super().get()
        self.params.update(kwargs)

        root = self.requests()
        if tag == "{http://sarws.ana.gov.br}ReservatorioSIN":
            series = SerieTemporalNis()
            for i in root[0]:
                try:
                    date = pd.to_datetime(i[6].text.strip())
                    code = i[0].text.strip()
                    series.volume.at[date, code] = i[2].text.strip()
                    series.height.at[date, code] = i[3].text.strip()
                    series.affluence.at[date, code] = i[4].text.strip()
                    series.flow.at[date, code] = i[5].text.strip()
                except AttributeError:
                    pass
            return series
        elif tag == "{http://sarws.ana.gov.br}ReservatorioNordeste":
            series = SerieTemporalNor()
            for i in root[1]:
                try:
                    date = pd.to_datetime(i[4].text.strip())
                    code = i[0].text.strip()
                    series.code_hydro = i[5].text.strip()
                    series.volume.at[date, code] = i[3].text.strip()
                    series.height.at[date, code] = i[2].text.strip()
                    series.capacity = i[6].text.strip()
                except AttributeError:
                    pass
            return series


