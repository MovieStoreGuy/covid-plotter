import requests
import logging
from urllib.parse import urljoin

from data.point import Point

HEC_ENDPOINT = "/services/collector/event"


class Splunk():

    def __init__(self, authtoken: str, domain:str = "http://localhost:8088") -> None:
        self._url = urljoin(domain, HEC_ENDPOINT)
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Splunk {authtoken}',
        }
        self._logger = logging.getLogger(__name__)

    def export(self, points: list[Point]) -> None:
        with requests.Session() as s:
            for p in points:
                blob = {
                    'time': p.timestamp().timestamp(),
                    'event': p.tags(),
                    'source': p.dataset(),
                }
                r = s.post(self._url, headers=self._headers, json=blob)
                try:
                    r.raise_for_status()
                except Exception as e:
                    self._logger.error(f'''Unable to post data to splunk hec due to: [{e}:{r.text}]''')
                    raise e
