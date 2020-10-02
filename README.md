# Mobility Database Interface

## Table of contents
* [General info](#general-info)
* [Getting Started](#getting-Started)
  *  [Prerequisites](#Prerequisites)
  *  [Installation](#Installation)
* [Related](#Related)
* [License](#License)

## General info
To be added

## Getting Started
To be added

### Prerequisites

Please note that the software provided was developed and run on macOS Catalina version 10.15.4 systems with Python 3.8.
While Python can run on a variety of systems, these instructions are written for the aforementioned specifications.
The repository does not contain the GTFS data, it must be downloaded.

### Installation

To correctly use and run this project, you must install all requirements. It is suggested to set up a virtual environment before proceeding to requirements installation. To set up and activate a python 3 virtual environment, enter the following commands:
```
$ pip install virtualenv
$ virtualenv -p python3 ENVNAME
$ source ENVNAME/bin/activate
```

Once your virtual environment is activated, enter the following command to install the project requirements:
```
$ pip install --default-timeout=120 -r requirements.txt
```

Note that you will also need the [gtfs-kit library](https://pypi.org/project/gtfs-kit/) to be installed on your local machine to run the project. To install it, enter the following command:
```
$ pip install gtfs-kit
```

To deactivate your virtual environment, enter the following command:
```
$ deactivate
```

If you are working with Intellij, it is possible to use this virtual environment within the IDE. To do so, follow the instructions to create a virtual environment in Intellij [here](https://www.jetbrains.com/help/idea/creating-virtual-environment.html).

## Related

- [gtfs-kit library](https://pypi.org/project/gtfs-kit/)

## License

Code licensed under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).
