#!/usr/bin/env -S python3 -dOt

import logging
import os
import typing
from concurrent.futures import ThreadPoolExecutor

from data.exporter import InfluxDB, Splunk
from data.collector import NSW, Persist

INFLUXDB_TOKEN: str = os.getenv('INFLUXDB_TOKEN')
SPLUNK_HEC_TOKEN: str = os.getenv('SPLUNK_HEC_TOKEN')

INFLUXDB_URL: str = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
SPLUNK_URL: str = os.getenv('SPLUNK_HEC_URL', 'http://localhost:8088')


def combine_job(exporters: list[typing.Callable], collect: typing.Callable, *args) -> None:
    logging.info(f'''Running collection job for {collect.__name__}''')
    for points in collect(*args):
        for export in exporters:
            export(points)
    logging.info(f'''Finished collection job for {collect.__name__}''')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    influx = InfluxDB(
        INFLUXDB_TOKEN,
        'covid-19',
        'covid-data',
        INFLUXDB_URL,
        {'Loc', 'Lon', 'lga_code19', 'lhd_2010_code', 'postcode'}, # High cardinality fields
    )

    splunk = Splunk(SPLUNK_HEC_TOKEN, domain=SPLUNK_URL)

    state = Persist(NSW())

    logging.info('Begining to collect state data')
    jobs = list()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for fn in [state.getCasesByAge, state.getCasesByLGA, state.getTestsByLGA, state.getCasesByLikelySource]:
            logging.info('Collecting new data set')
            future = pool.submit(combine_job, [influx.export, splunk.export], fn, 100_000, 0, None)
            jobs.append(future)
    for j in jobs:
        logging.info('Job status information %s', j.result())

    logging.info('finished reading all data')
