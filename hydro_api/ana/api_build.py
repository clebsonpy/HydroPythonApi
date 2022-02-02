from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET
import requests


class ApiBuild(metaclass=ABCMeta):

    source = None

    def requests(self):
        if type(self.url) is list:
            root = []
            for url in self.url:
                response = requests.get(url, self.params, timeout=180)
                if not response:
                    raise ConnectionError
                tree = ET.ElementTree(ET.fromstring(response.content))
                root.append(tree.getroot())
        else:
            if self.source == 'ANA':
                response = requests.get(self.url, self.params, timeout=180)
                if not response:
                    raise ConnectionError

                tree = ET.ElementTree(ET.fromstring(response.content))
                root = tree.getroot()

            elif self.source == 'INMET':
                response = requests.get(self.url, timeout=180)
                root = response.json()

            else:
                root = None

        return root

    def _get_text(self, element):
        try:
            return element.text
        
        except AttributeError:
            return None

    @abstractmethod
    def _get(self, **kwargs):
        if len(kwargs) > 0:
            for i in kwargs:
                if i in self.params:
                    pass
                else:
                    raise KeyError
        else:
            pass
