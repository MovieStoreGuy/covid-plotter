import typing
from data.point import Point

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision


class InfluxDB():

    def __init__(self, token: str, org: str, default_bucket: str,
                 url: str = "http://localhost:8086", drop_keys: typing.Iterable = None) -> None:
        self._api = influxdb_client.InfluxDBClient(
            url=url,
            org=org,
            token=token,
        )
        self._defaultBucket = default_bucket
        self._defaultOrg = org
        self._drop_keys = drop_keys

    def check(self) -> None:
        assert not self._api.health().status() == 'fail'

    def export(self, points: list[Point]) -> None:
        writer = self._api.write_api(write_options=SYNCHRONOUS)
        writer.write(
            self._defaultBucket,
            self._defaultOrg,
            [to_influxdb_point(p, self._drop_keys) for p in points],
        )
        writer.close()


def to_influxdb_point(pt: Point, drop_keys: typing.Iterable) -> influxdb_client.Point:
    p = influxdb_client.Point(pt.dataset())\
        .time(pt.timestamp(), WritePrecision.NS)\
        .field(pt.name(), pt.value())

    for k, v in {k: v for k, v in pt.tags().items() if not k in drop_keys}.items():
        p.tag(k, v)

    return p
