#!/usr/bin/env -S python3 -dOt

import logging
import typing
from concurrent.futures import ThreadPoolExecutor

from data.exporter import InfluxDB
from data.collector import NSW, Persist


def combine_job(export: typing.Callable, collect: typing.Callable, *args) -> None:
    logging.info(f'''Running collection job for {collect.__name__}''')
    for points in collect(*args):
        export(points)
    logging.info(f'''Finished collection job for {collect.__name__}''')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, encoding='UTF-8')

    exporter = InfluxDB(
        '5iOiu00R7ntYQTE0_egua_LBIzaoJvxYUP62doDjQ4Z1UNmUUlvNjxMa9nBwcP13rhsALBn0clJ9hp_gVKBSYA==',
        'covid-19',
        'covid-data',
    )

    state = Persist(NSW())

    logging.info('Begining to collect state data')
    jobs = list()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for fn in [state.getCasesByAge, state.getCasesByLGA, state.getTestsByLGA, state.getCasesByLikelySource]:
            logging.info('Collecting new data set')
            future = pool.submit(combine_job, exporter.export, fn, 100, 0, None)
            jobs.append(future)
    for j in jobs:
        logging.info('Job status information %s', j.result())

    logging.info('finished reading all data')
