# Trains

ThoughtWorks Trains Solution by Fernando Felix do Nascimento Junior.

See [PROBLEM](/PROBLEM.md).

## Module artifacts

The module `trains.py` contains basically a distance Graph class and a set of function to help compute route distances and counts.

Bellow an abstract of the module artifacts.

* Graph class: An unidireccional distance graph
* route_distance function: Return the total route distance given a distance graph
* shortest_route_distance function: Return the shortest route distance between a starting and ending routes based on
nearest neighbour algorithm
* count_routes_by_stops function: Count routes recursively between a start node and an end node based on number of stops
criterion
* count_routes_by_max_distance: Count routes recursively between a start node and an end node based on a maximum
distance criterion.

## Tools

* [coverage.py](https://coverage.readthedocs.org/) - Code coverage measurement.
* [Flake8](https://flake8.readthedocs.org/) - Modular source code checker: pep8, pyflakes and co.
* [pytest](http://pytest.org/) - A mature full-featured Python testing tool.
* [setuptools](https://pythonhosted.org/setuptools/setuptools.html) - Easily download, build, install, upgrade, and uninstall distribution packages.
* [tox](https://tox.readthedocs.org/) - Auto builds and tests distributions in multiple Python versions using virtualenvs.

## Structure

```sh
├── Makefile  # Automates useful tasks to use with make, a build automation tool
├── MANIFEST.in  # Specifies extra resources to add in distributions packages
├── PROBLEM.md  # Specifies the train problem 
├── README.md  # Details how to use the solution
├── requirements.txt  # Contains dependencies of the project to be installed using pip
├── trains.py  # The core code of the solution
├── setup.cfg  # Configures some settings of the tools used in the project
├── setup.py  # Contains information needed to build distributions with setuptools
├── tests.py  # Provides some automated tests to run with pytest
└── tox.ini  # Defines test environments to run with tox
```


## Usage

Create virtualenv
`virtualenv env && . env/bin/activate`

Install code style and test requirements
`pip insall -r requirements.txt`

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
`coverage report --show-missing`

Output:

```
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
tests.py       33      0   100%
trains.py      86     11    87%   135-153
-----------------------------------------
TOTAL         119     11    91%
```

Build, test and coverage the solution in different python verions
`tox`
