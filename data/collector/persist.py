import typing
import os
import hashlib
import logging

from data.collector import State
from data.point.point import Point


class Persist(State):

    def __init__(self, wrap: State, statedir: str = "cache/") -> None:
        self._logger = logging.getLogger(__name__)
        self._wrap = wrap
        self._store = os.path.join(os.getcwd(), statedir)
        if not os.path.isdir(self._store):
            os.mkdir(self._store)

    def _persistState(self, method: typing.Callable, limit: int = 100, offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point], None, None]:
        statefile = method.__name__ + f'-{limit}-' + hashlib.md5(repr(query).encode('utf-8')).hexdigest()
        # Need to figure out restarting from last known state
        try:
            with open(os.path.join(self._store, statefile), "r") as f:
                for line in f:
                    offset = int(line.split()[0])
        except (OSError, IOError) as e:
            self._logger.debug(f'Unable to open state file due to {e}')

        self._logger.info(f'Starting to read data {method.__name__}:{offset}')
        with open(os.path.join(self._store, statefile), "w") as s:
            for pts in method(limit, offset, query):
                yield pts
                s.seek(0)
                s.truncate(0)
                s.write(f'{offset}\n')
                s.flush()
                offset += limit
                

    def getCasesByAge(self, limit: int, offset: int, query: str) -> typing.Generator[list[Point], None, None]:
        return self._persistState(self._wrap.getCasesByAge, limit, offset, query)

    def getCasesByLGA(self, limit: int, offset: int, query: str) -> typing.Generator[list[Point], None, None]:
        return self._persistState(self._wrap.getCasesByLGA, limit, offset, query)

    def getCasesByLikelySource(self, limit: int, offset: int, query: str) -> typing.Generator[list[Point], None, None]:
        return self._persistState(self._wrap.getCasesByLikelySource, limit, offset, query)

    def getTestsByLGA(self, limit: int, offset: int, query: str) -> typing.Generator[list[Point], None, None]:
        return self._persistState(self._wrap.getTestsByLGA, limit, offset, query)
