import time
import random
from eht_influxdb_client.timebin import TimeBin

tb = TimeBin(1.0)  # 1.0 second bins is the default

count = 0
while count < 10:
    datapoint = random.randint(1,10)
    tb.point(time.time(), datapoint)
    tuples = tb.gettuples()
    if tuples:
        print(tuples)  # [(t, value)] where times are exactly 1.0s apart
    time.sleep(1.0 + datapoint*0.01)
    count += 1
