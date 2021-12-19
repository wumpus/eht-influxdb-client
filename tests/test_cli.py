from eht_influxdb_client.cli import main


def test_print_config(capsys):
    args = 'print-config'.split()
    main(args=args)
    out, err = capsys.readouterr()
    assert len(err) == 0
    assert len(out) > 0
