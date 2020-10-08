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

To correctly use and run this project, you must install all requirements. First, make sure Python 3.8+ and Pip are installed.
```
$ python3 --version
$ pip --version
```

If Python 3.8+ is not installed on your computer, get it with Homebrew (Mac) :
```
$ brew install python3.8
```
or with Apt (Linux) :
```
$ sudo apt-get install python3.8
```

If Pip is not installed on your computer, get it with the following commands :
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
```

Also, make sure you will need both GDAL and RTree (Libspatialindex) libraries installed on your computer :
```
$ brew install GDAL
$ brew install spatialindex
```

It is suggested to set up a virtual environment before proceeding to further requirements installation. To set up and activate a Python 3 virtual environment, enter the following commands:
```
$ pip install virtualenv
$ virtualenv -p python3 env
$ source env/bin/activate
```

Once your virtual environment is activated, enter the following command to install the project requirements:
```
(env) $ pip install --default-timeout=120 -r requirements.txt
```

Note that you will also need the [gtfs-kit library](https://pypi.org/project/gtfs-kit/) to be installed on your local machine to run the project. To install it, enter the following command:
```
(env) $ pip install gtfs-kit
```

To deactivate your virtual environment, enter the following command:
```
(end) $ deactivate
```

If you are working with Intellij, it is possible to use this virtual environment within the IDE. To do so, follow the instructions to create a virtual environment in Intellij [here](https://www.jetbrains.com/help/idea/creating-virtual-environment.html).

## Related

- [gtfs-kit library](https://pypi.org/project/gtfs-kit/)

## License

Code licensed under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).
