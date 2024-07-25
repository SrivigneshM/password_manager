# password_manager
Git repository to maintain python code-base for password management utility

## Prerequisites:

| Software                                                       | Version |
|----------------------------------------------------------------|---------|
| [Python](https://docs.python-guide.org/starting/install3/osx/) | 3.7.7   |
| [sqlite](https://www.sqlite.org/download.html)                 | 3.28.0  |

## Installation:

- Download and run
```sh
$ curl -LSf -u "username:password" -O https://sriv.jfrog.io/artifactory/password-manager-local/simvault-password-manager/3.0.0/simvault-password-manager-3.0.0.tar.gz
$ tar -xvf simvault-password-manager-3.0.0.tar.gz
$ cd simvault-password-manager-3.0.0
$ chmod -R 700 startup.sh
$ sh startup.sh
```
- Add below line to /etc/hosts file

```sh
127.0.0.1 localhost
```
- Invoke the URL from browser http://localhost:5033/

## Setup virtual environment for development

```sh
$ python3 -m venv ENV
$ source ENV/bin/activate
$ pip3.7 install -r requirements.txt
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
$ sh pytest.sh
```

## Packaging and distribution

```sh
$ python3 -m pip install --upgrade build
$ python3 -m build
$ source ENV/bin/activate
$ twine upload -r local dist/simvault-password-manager-3.0.0.tar.gz --config-file .pypirc
```


## Security

```sh
$ cd ssl
$ openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout simvault.key -out simvault.crt -config req.cnf -sha256
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout license.key -out license.crt
$ openssl pkcs12 -export -out license.p12 -inkey license.key -in license.crt
```
