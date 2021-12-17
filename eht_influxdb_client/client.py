import os
import os.path
import configparser
from urllib3 import Retry

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.domain.write_precision import WritePrecision


class WrapInfluxDBClient(InfluxDBClient):
    def __init__(self, *args, **kwargs):
        if 'bucket' in kwargs:
            self._bucket = kwargs['bucket']
            del kwargs['bucket']
        return super().__init__(*args, **kwargs)

    @property
    def bucket(self):
        return self._bucket

    @classmethod
    def from_config_file(cls, fname, *args, **kwargs):
        '''Test for some common mistakes that cause inscrutable errors:
        file not found => KeyError
        inline comments in the ini file are not stripped, and if in the URL,
        can easily result in a weird error like:
        "FluxCsvParserException: Unable to parse CSV response. FluxTable definition was not found."
        If the bucket name is in the config file
        '''
        fname = os.path.expandvars(os.path.expanduser(fname))
        if not os.path.isfile(fname):
            raise ValueError('ini file does not exist: '+str(fname))

        config = configparser.ConfigParser()
        config.read(fname)

        if 'influx2' not in config:
            raise ValueError('config file lacks an [influx2] section')

        ci = config['influx2']
        for key, value in ci.items():
            value = value.replace('"', '')
            if ' ' in value or '#' in value:
                raise ValueError('from_config_file: saw a space or # in {}... hint: inline comments are not valid in config files'.format(key))
            if key in kwargs:
                print('from_config_file: letting keyword override config file for key', key)
            else:
                kwargs[key] = value

        if 'bucket' in kwargs:
            bucket = kwargs['bucket']
            del kwargs['bucket']
        else:
            bucket = None

        instance = cls(*args, **kwargs)

        if bucket is not None:
            instance._bucket = bucket

        return instance


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
