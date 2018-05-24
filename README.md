# Trains

ThoughtWorks Trains Solution by Fernando Felix do Nascimento Junior.

See [PROBLEM](/PROBLEM.md).

## Structure

```sh
├── PROBLEM.md  # Specifies the train problem
├── README.md  # Details how to use the solution
├── requirements.txt  # Contains dependencies of the project to be installed using pip
├── trains.py  # Module with core code of the solution
├── setup.cfg  # Configures some settings of the tools used in the project
├── setup.py  # Contains information needed to build distributions with setuptools
├── tests.py  # Provides some automated tests to run with pytest
└── tox.ini  # Defines test environments to run with tox
└── travis.yml  # Continuous integration configuration
```

## Module artifacts

The module `trains.py` contains basically a distance Graph class and a set of function to help compute route distances and counts.

Bellow an abstract of the module artifacts.

* Graph class: An unidireccional distance graph
* find_route_path function: Return the shortest or largest route distance between a starting and ending routes based on nearest neighbour algorithm


## Tools

* [coverage.py](https://coverage.readthedocs.org/) - Code coverage measurement.
* [Flake8](https://flake8.readthedocs.org/) - Modular source code checker: pep8, pyflakes and co.
* [pytest](http://pytest.org/) - A mature full-featured Python testing tool.
* [setuptools](https://pythonhosted.org/setuptools/setuptools.html) - Easily download, build, install, upgrade, and uninstall distribution packages.
* [tox](https://tox.readthedocs.org/) - Auto builds and tests distributions in multiple Python versions using virtualenvs.


## Usage

Create virtualenv
`virtualenv env && . env/bin/activate`

Install code style and test requirements
`pip install -r requirements.txt`

Run ThoughtWorks trains solution
`python trains.py`

Output
```
9
5
13
22
NO SUCH ROUTE
2
3
9
9
7
```

Run all provided tests for the solution
`py.test`

Run code coverage
`coverage erase && coverage run -m py.test && coverage report --show-missing`

Output:
```
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
tests.py       33      0   100%
trains.py      86     11    87%   135-153
-----------------------------------------
TOTAL         119     11    91%
```

Build, test and coverage the solution in different python versions
`tox`
