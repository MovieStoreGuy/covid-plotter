#!/usr/bin/env -S python3 -dOt

import logging
import typing
from concurrent.futures import ThreadPoolExecutor

from data.exporter import InfluxDB
from data.collector import NSW


def combine_job(export: typing.Callable, collect: typing.Callable, *args) -> None:
    logging.info(f'''Running collection job for {collect.__name__}''')
    export(collect(args))
    logging.info(f'''Finished collection job for {collect.__name__}''')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, encoding='UTF-8')

    exporter = InfluxDB(
        '5iOiu00R7ntYQTE0_egua_LBIzaoJvxYUP62doDjQ4Z1UNmUUlvNjxMa9nBwcP13rhsALBn0clJ9hp_gVKBSYA==',
        'covid-19',
        'covid-data',
    )

    state = NSW()

    logging.info('Begining to collect state data')
    # with ThreadPoolExecutor(max_workers=4) as pool:
    #     for fn in [state.getCasesByAge, state.getCasesByLGA, state.getTestsByLGA, state.getCasesByLikelySource]:
    #         logging.info('Collecting new data set')
    #         pool.submit(combine_job, exporter.export, fn, 100_000_000)
    for pts in state.getCasesByAge():
        print(pts)

    logging.info('finished reading all data')
