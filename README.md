# Medical Records Management System

The system is implemented in the form of web application. It was developed using Python and [Flask](http://flask.pocoo.org/)

The system automatically updates critical status based on factors such as haemoglobin.

## Getting Started

The med.db file contains the sqlite record for the patients.

### Prerequisites

python3

[Flask](http://flask.pocoo.org/)

[flask-login](https://flask-login.readthedocs.io/en/latest/)

### Installing

```
pip3 install flask
```
```
pip3 install Flask-Login
```

## Deployment

To run the app 

```
export FLASK_APP=login.py
```
```
flask run
```
For running on a server
```
flask run --host=0.0.0.0
```

The default credentials are username:admin and password:admin

