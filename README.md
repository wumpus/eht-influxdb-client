# eht-influx-client

This package provides a client to deliver monitoring information about
the Event Horizon Telescope to an InfluxDB-based datastore.

It provides a simple interface to the EHT's standard monitoring setup, which includes:

* A local logfile at each station
* A local InfluxDB database at each station
* A global InfluxDB database in the cloud
* Tools for re-inserting logged data into InfluxDB

## Usage

The interface for this client is intended to be similar to the official influxdb client:

```
    import pandas as pd
    from eht_influx_client import EHTInfluxDBClient

    df = pd.DataFrame([{'station': 'Kp', 'pps_offset': -3, 'timestamp': 1617672549204824064}])

    client = EHTInfluxDBClient.from_config_file('influx_config.ini')
    write_api = client.write_api()
    write_api.write(record=df,
                    data_frame_measurement_name='pps_offset',
                    data_frame_tag_columns=['station'],
    )
    write_api.close()
    client.close()
```

Behind the scenes, the `influxdb_confg.ini file` controls a lot more configuration
than the usual Influx client, including the bucket name, one or more InfluxDB servers, the
location of a logfile, a retry policy, and error reporting. The default `write_options`
is `ASYNCHRONOUS`.

Note that `write_options=ASYNCHRONOUS` is incompatible with creating
your own Python multiprocessing pool.

## Configuration

To see the full range of configuring the client, use the cli command

`$ eht-influx-client print-config > influx_config.ini`

## Replaying logged CSV data into InfluxDB

InfluxDB has a standard method of inserting bulk data contained in a csv file, by adding
an additional line at the top:

```
#datatype measurement,tag,long,dateTime:number
measurement,station,pps_offset,timestamp
pps,KP,0,1617672549204824064
```

This CSV is inserted into a database with:

`$ influx write -h db_ip:db_port -b bucket -f foo.csv`

And can be read back out with:

`$ influx ...`

## Replaying logged JSONL data into InfluxDB

## Binning

To support lower time precisions, it is useful to have a function
which interpolates data values into exact time bins.

```
import time
import random
from eht_influx_client.timebin import TimeBin

tb = TimeBin(1.0)  # 1.0 second bins is the default

while True:
    datapoint = random.randint(1,10)
    tb.point(time.time(), datapoint)
    tuples = tb.gettuples()
    if tuples:
       print(tuples)  # [(t, value)] where times are exactly 1.0s apart
    time.sleep(1.0 + datapoint*0.01)
```

## TODO

examine influxdb_client to see how they test

test .read_config_file():
fnf
inline comments
lack of bucket
_test vs _prod

check the incoming data-or-df to make sure it has a 'timestamp'
provide helpers to go from Python time to iso8601/rfc3339 and back (and what's the difference?)

implement multiple influx databases in the config
implement jsonl logfile with a separate json schema (?)
make the timestamp the first field of csv and jsonl for sorting/grepping ease

implement jsonl logfile replay into the database
implement database to jsonl logfile
