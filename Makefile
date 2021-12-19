.PHONY: init test clean_coverage test_coverage distclean distcheck dist install

init:
	pip install --use-feature=in-tree-build .

test_scripts:
	PYTHONPATH=.:scripts python scripts/timebin_example.py

test_tests:
	PYTHONPATH=. py.test --doctest-modules tests -v -v

test: test_tests test_scripts

clean_coverage:
	rm -f .coverage

test_coverage: clean_coverage
	#PYTHONPATH=. coverage run -a --source=eht_influxdb_client
	PYTHONPATH=. py.test --doctest-modules --cov-report=xml --cov-append --cov eht_influxdb_client tests -v -v
	coverage report

distclean:
	rm -rf dist/

distcheck: distclean
	python ./setup.py sdist
	twine check dist/*

dist: distclean
	echo "reminder, you must have tagged this commit or you'll end up failing"
	echo "  git tag v0.x.x"
	echo "  git push --tags"
	python ./setup.py sdist
	twine upload dist/* -r pypi

install:
	python ./setup.py install

