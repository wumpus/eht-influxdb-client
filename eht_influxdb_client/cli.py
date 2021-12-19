from argparse import ArgumentParser

import eht_influxdb_client


def main(args=None):
    parser = ArgumentParser(description='EHT InfluxDB client command line tool')

    parser.add_argument('verb')

    args = parser.parse_args(args=args)

    if args.verb == 'print-config':
        print('foo')
