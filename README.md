# Django Test app

This is an example Django app that uses python 3.7 and SQLite as persistence storage.

[Django official documentation](https://docs.djangoproject.com/en/2.2/)

## Models

The db tables is reflected into the Django models and in order to use with an empty sqlite db, running make migrations and migrate commands is needed.


```sh
# run this commands into the project root
$ python manage.py makemigrations
$ python manage.py migrate
```

## Endpoints

The url config of the notifications service app is included into the main urls config file. `notification_service.urls`

### Main urls config file

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('notification_service.urls'))
]
```

### Application urls

```python
from django.urls import path
from .service import Service

urlpatterns = [
    path('notification/', Service.label_parsing),
]
```

### Application service

The core is the application service that does the need stuff to manage the `notification service` flow.

```python
from datetime import date

from .logger import LoggerService
from .models import Customers, NotificationCounters, Notifications
from django.http import HttpResponse
from django.views import View
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F
import re

class Service(View):

    " Get labels from the model" \
    " The cache are not implemented so the query is executed each time "
    def label_parsing(request):
        if request.method == 'POST':
            try:

                LoggerService.set_log_level('info').log('Getting labels from customers table')

                queryset = Customers.objects.values('notification_label', 'id')

                " truncate at 300 "
                notification = str(request.body)[:300] if len(str(request.body)) > 300 else str(request.body)

                customers_matches = Service.label_matches_service(queryset, notification)
                
                ............
```

### Application logger

The service uses a custom dynamic application logger and one file for each log level will be wrote.
Take a look at the configuration below. The base logging class is the Django default one. The logs file will be placed into the logs folder into the project root.

```python
logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'handlers': {
                'logfile': {
                    'level': level.upper(),
                    'class': 'logging.FileHandler',
                    'filename': 'logs/' + level.upper() + '.log',
                    'formatter': 'simple'
                },
            },
            'loggers': {
                'notificationService': {
                    'handlers': ['logfile'],
                    'level': level.upper()
                },
            },
        })
```

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

