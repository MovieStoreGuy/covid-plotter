from data import point
from data.point import Point

import pandas as pd

class CSV():

  @staticmethod
  def export(points: list[Point]) -> None:
    points.sort(lambda x: x.timestamp())

    pd.DataFrame([vars(o) for o in point])