import abc
import typing
from data.point import Point


class State(metaclass=abc.ABCMeta):
    '''
    State defines the abstract methods to collect covid data from a given state.
    '''
    @abc.abstractclassmethod
    def getCasesByLGA(self,
                      limit: int = 100,
                      offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point],
                                                             None,
                                                             None]: ...

    @abc.abstractclassmethod
    def getTestsByLGA(self,
                      limit: int = 100,
                      offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point],
                                                             None,
                                                             None]: ...

    @abc.abstractclassmethod
    def getCasesByLikelySource(self,
                               limit: int = 100,
                               offset: int = 0,
                               query: str = None) -> typing.Generator[list[Point],
                                                                      None,
                                                                      None]: ...

    @abc.abstractclassmethod
    def getCasesByAge(self,
                      limit: int = 100,
                      offset: int = 0,
                      query: str = None) -> typing.Generator[list[Point],
                                                             None,
                                                             None]: ...
