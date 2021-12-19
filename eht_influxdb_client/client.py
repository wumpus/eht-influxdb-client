import os
import os.path
from urllib3 import Retry

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.domain.write_precision import WritePrecision

from . import config


class WrapInfluxDBClient(InfluxDBClient):
    def __init__(self, *args, **kwargs):
        self._bucket = kwargs['bucket'].pop(None)
        return super().__init__(*args, **kwargs)

    @property
    def bucket(self):
        return self._bucket

    @classmethod
    def from_config_file(cls, fname, *args, **kwargs):
        kwargs = config.read_config_file(fname, **kwargs)

        return cls(*args, **kwargs)


def write_points(write_api, bucket, measurement, points, t, station, write_precision=WritePrecision.S):
    '''Write data from a single timestamp to Influx
    Provides these services:
    * local logging, in case data needs to be re-inserted later
    * writing to more than 1 Influx database, for example local and global
    * asynchronous operation, so that the main application loop is not delayed during internet outages
    '''
    if 'PYTEST_CURRENT_TEST' in os.environment:
        # XXX extend this check to not only pytest environments
        if not bucket.endswith('_test'):
            raise AssertionError('when running inside PyTest, bucket names must end with "_test"')

    objs = []
    for p in points:
        objs.append(Point(measurement).tag('station', station).time(t, write_precision=write_precision))

    try:
        # if batched: success_callback, error_callback, retry_callback ... not sure if they care called for async
        # if batched, write_api.flush() does what you think
        async_result = write_api.write(bucket=bucket, record=p)
    except InfluxDBError:
        # I have never seen this happen XXX try stopping the influx instance mid-write
        raise

    if async_result is not None:
        print('type', type(async_result))  # type <class 'multiprocessing.pool.ApplyResult'>
        print(async_result.get())  # None
