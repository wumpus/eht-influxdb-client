import os
import configparser


example_config = '''
[eht_influx]
# note that comments have to be on lines by themselves
# no https on localhost, elsewise you probably do want https
url: "http://localhost:8086/"
org: "eht"
bucket: "vlbimon_test"
token: "<FILL ME IN>"

# this next section is not yet implemented
url2: "http://localhost:8086/"
org2: "eht"
bucket2: "vlbimon_test"
token2: "<FILL ME IN>"

# these are not yet implemented, either
csvlogfile: /path/to/logfile/foo.csv
jsonlogfile: /path/to/logfile/foo.jsonl
'''


allowed_keys = {'url', 'org', 'bucket', 'token'}
# 'url2', 'org2', 'bucket2', 'token2'
# 'csvlogfile', 'jsonlogfile'


def read_config_file(fname, **kwargs):
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

    if 'eht_influx' not in config:
        raise ValueError('config file lacks an [eht_influx] section')

    ci = config['eht_influx']
    for key, value in ci.items():
        value = value.replace('"', '')
        if '#' in value:
            print('value', value)
            raise ValueError('from_config_file: saw a space or # in {}... hint: inline comments are not valid in config files'.format(key))
        if key in kwargs:
            print('from_config_file: letting keyword override config file for key', key)
        else:
            kwargs[key] = value

    return kwargs


def print_config():
    print(example_config)
