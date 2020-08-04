from abc import ABCMeta, abstractmethod
import xml.etree.ElementTree as ET
import requests


class ApiBiuld(metaclass=ABCMeta):

    def requests(self):
        if type(self.url) is list:
            root = []
            for url in self.url:
                response = requests.get(url, self.params)
                if not response:
                    raise ConnectionError
                tree = ET.ElementTree(ET.fromstring(response.content))
                root.append(tree.getroot())
        else:
            response = requests.get(self.url, self.params)
            if not response:
                raise ConnectionError

            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()

        return root

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
