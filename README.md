DEVELOPMENT README
==================

* cd out of this project directory, then install pyenv

* cd back to the directory to have pyenv shim to Python 2.7.10

* Run `pyenv virtualenv autoundotests` to create a virtualenv for
  this project. This ensures that this project has its own set of
  libraries that don't conflict with other python projects in your
  development machine.

* Activate the virtualenv with `pyenv activate autoundotests`

* Install tox with `pip install tox`


RUNNING TESTS
=============

* Run `tox -e app` to run the app tests

* Run `tox -e meta` to run the metatests (tests that test the tests!)

NOTE: Something about the coverage library prevents it from reading the
coverage data on the first run (or right after you recreate a tox env).
Subsequent runs of the test should be successful in collecting the test
coverage data, however.
