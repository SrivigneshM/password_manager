# password_manager
Git repository to maintain python code-base for password management utility

## Prerequisites:

| Software                                                       | Version |
|----------------------------------------------------------------|---------|
| [Python](https://docs.python-guide.org/starting/install3/osx/) | 3.7.7   |
| [sqlite](https://www.sqlite.org/download.html)                 | 3.28.0  |

## How to run the app?

```sh
$ sh startup.sh
```

## How to use the app?

Invoke the URL from browser http://localhost:5000/

## Setup virtual environment for development

```sh
$ python3 -m venv ENV
$ . ENV/bin/activate
$ ./ENV/bin/pip3.7 install -r requirements.txt
```

## Create and open test database

```sh
$ sqlite3
$ sqlite3 test_password_manager.db
$ .open ./test_password_manager.db
$ .read schema.sql
$ .mode column
$ .header on
```
DB design: click [here](schema.sql)

## Run pytest

```sh
$ ./ENV/bin/pip3.7 install -r test-requirements.txt
$ sh pytest.sh
```
