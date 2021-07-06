import pandas as pd
from ..api_biuld import ApiBiuld


class _Entity:

    def __init__(self, code, name, abbreviation):
        self.code = code
        self.name = name
        self.abbreviation = abbreviation

    def __str__(self):
        return f"Code: {self.code}\nName: {self.name}\nSigla: {self.abbreviation}"

    def __repr__(self):
        return f"{self.abbreviation} - {self.name}"


class EntityApi(ApiBiuld):
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroEntidades'
    params = {'codEntidade': ''}

    def __init__(self, code_entity=''):
        kwargs = {'codEntidade': code_entity}
        super()._get(**kwargs)

        self.params.update(kwargs)
        self.entities = pd.DataFrame(columns=['Name', 'Code', 'Abbr']).set_index('Code')
        root = self.requests()
        self._get(root)

    def __getitem__(self, item) -> _Entity:
        entity = self.entities.loc[item]
        return _Entity(name=entity.Name, code=item, abbreviation=entity.Abbr)

    def _get(self, root):
        try:
            for entity in root.iter('Table'):
                code_entity = entity.find('Codigo').text
                self.entities.at[code_entity, 'Name'] = entity.find('Nome').text
                self.entities.at[code_entity, 'Abbr'] = entity.find('Sigla').text
        except:
            return False

        return True
