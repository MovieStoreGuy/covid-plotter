import datetime
import typing
import requests
import logging

from urllib.parse import urljoin
from dateutil.parser import parse

from data.collector.core import State
from data.point import Point


class NSW(State):
    '''
    A class to interact with the data published from https://data.nsw.gov.au/nsw-covid-19-data
    '''

    NSW_DATA_BASE = "https://data.nsw.gov.au"
    NSW_DATA_SEARCH = "data/api/3/action/datastore_search"

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def _collectCKANData(self, resource_id: str, limit: int = 100, offset: int = 0,
                         query: typing.Union[str, None] = None) -> typing.Generator[list[dict[str:str]], None, None]:
        q = {
            'limit': limit,
            'offset': offset,
            'resource_id': resource_id,
        }

        if query is not None:
            q['q'] = query

        session = requests.session()

        r = session.get(
            urljoin(
                self.NSW_DATA_BASE,
                self.NSW_DATA_SEARCH),
            params=q)
        r.raise_for_status()

        data = r.json().get('result', {})

        records = data.get('records', [])

        while not len(records) == 0:
            yield records
            next = data.get('_links', {}).get('next', "")
            u = urljoin(self.NSW_DATA_BASE, f'/data{next}')
            self._logger.info(f'Attempting to read data: {u}')
            r = session.get(u)
            r.raise_for_status()
            data = r.json().get('result', {})
            records = data.get('records', [])

    def getCasesByLGA(self, limit: int = 100, offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point], None, None]:
        ''' Fetches time stamped data on impacted LGAs with known cases '''
        for data in self._collectCKANData('21304414-1ff1-4243-a5d2-f52778048b29', limit, offset, query):
            pts = list(map(lambda p: NSWPoint('lga-venue-data', 'covid.nsw.exposure-venues', p), data))
            yield pts

    def getCasesByLikelySource(self, limit: int = 100, offset: int = 0,
                               query: str = None) -> typing.Generator[list[Point], None, None]:
        for data in self._collectCKANData('2776dbb8-f807-4fb2-b1ed-184a6fc2c8aa', limit, offset, query):
            pts = list(map(lambda p: NSWPoint('case-data', 'covid.nsw.by-location', p), data))
            yield pts

    def getTestsByLGA(self, limit: int = 100, offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point], None, None]:
        for data in self._collectCKANData('945c6204-272a-4cad-8e33-dde791f5059a', limit, offset, query):
            pts = list(map(lambda p: NSWPoint('testing-data', 'covid.nsw.tests', p), data))
            yield pts

    def getCasesByAge(self, limit: int = 100, offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point], None, None]:
        for data in self._collectCKANData('24b34cb5-8b01-4008-9d93-d14cf5518aec', limit, offset, query):
            pts = list(map(lambda x: NSWPoint('cases-by-age', 'covid.nsw.by-age', x), data))
            yield pts


class NSWPoint(Point):
    def __init__(self, dataset: str, name: str, data: dict[str:str]) -> None:
        stamp = data.pop('notification_date', None) or data.pop('test_date', None)
        if stamp is None:
            raise ValueError('missing known date field')
        self._timestamp = parse(stamp)
        self._name = name
        self._dataset = dataset

        self._tags = {k: notblank(v) for k, v in data.items()}

    def value(self) -> typing.Union[int, float]:
        return 1

    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    def name(self) -> str:
        return self._name

    def dataset(self) -> str:
        return self._dataset

    def tags(self) -> dict[str:str]:
        return self._tags


def notblank(s: typing.Union[str, None]) -> str:
    return s or 'unknown'
