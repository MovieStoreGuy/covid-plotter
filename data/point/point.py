import abc
import datetime
import typing


class Point(metaclass=abc.ABCMeta):
    '''
      Point defines a universal class that allows data exporters
      to convert their internal type while data collectors implement
      the concrete type.
    '''

    @abc.abstractclassmethod
    def timestamp(self) -> datetime.datetime:
        '''Returns the timestamp associated with the point'''
        pass

    @abc.abstractclassmethod
    def dataset(self) -> str:
        '''Returns the dataset name associated with the point'''
        pass

    @abc.abstractclassmethod
    def tags(self) -> dict[str:str]:
        '''Returns the tags associated with the point'''
        pass

    @abc.abstractclassmethod
    def value(self) -> typing.Union[int, float]:
        '''Returns the value associated with the point'''
        pass

    @abc.abstractclassmethod
    def name(self) -> str:
        '''Returns the name associated with the point'''
        pass
