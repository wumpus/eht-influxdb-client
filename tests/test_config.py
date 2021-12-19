from collections.abc import Collection

import eht_influxdb_client.config


def test_read_config_file(fs):
    fs.create_file('a')
    with open('a', 'w') as fd:
        print(eht_influxdb_client.config.example_config, file=fd)
    assert isinstance(eht_influxdb_client.config.read_config_file('a'), Collection), 'correct return value for the example config'
