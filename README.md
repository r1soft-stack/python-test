# Django Test app

This is an example Django app that uses python 3.7 and SQLite as persistence storage.

## Models

The db tables is reflected into the Django models and in order to use with an empty sqlite db, running make migrations a migrate is needed.


```sh
# run this commands into the project root
$ python manage.py makemigrations
$ python manage.py migrate
```

[Django official documentation](https://docs.djangoproject.com/en/2.2/)

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. Alternatively you
can use foreman and gunicorn to run the server locally (after copying
`dev.env` to `.env`):

```sh
$ foreman start
```

## Notification service endpoint

The notification service endpoint is available here `http://localhost:8000/service/notification/`. It accepts only POST method, the GET one will be ignored.
The service accepts a row body and the message will be truncated at 300 characters length.

