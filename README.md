# password_manager
Git repository to maintain python code-base for password management utility

## Prerequisites:

| Software                                                       | Version |
|----------------------------------------------------------------|---------|
| [Python](https://docs.python-guide.org/starting/install3/osx/) | 3.7.7   |
| [sqlite](https://www.sqlite.org/download.html)                 | 3.28.0  |

## Setup virtual environment for development

```sh
$ python3 -m venv ENV
$ . ENV/bin/activate
$ ./ENV/bin/pip3.7 install -r requirements.txt
```

## Run flask app

```sh
$ python3 src/app.py
```

## Invoke flask app

Invoke the URL from browser http://localhost:5000/

## Create and open database

```sh
$ sqlite3
$ sqlite3 password_manager.db
$ .open ./password_manager.db
$ .read schema.sql
$ .mode column
$ .header on
```
DB design: click [here](schema.sql)

## Run pytest

```sh
$ ./ENV/bin/pip3.7 install -r test-requirements.txt
$ sh pytest.sh tests/test_signup_api.py
```
