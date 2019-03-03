"""

This class exposes all the methods to manage the message

The `urlpatterns` are binded to those methods, following the controller pattern.

THere is an implementation of custom logging service. An example below.
Example:  LoggerService.set_log_level('warning').log({"name": "my name", "levelname": "the message", "message": "message"})
Log format: [2019-03-02 22:01:48] WARNING {'message': 'message', 'name': 'my name', 'levelname': 'the message'}

"""

from .logger import LoggerService
from .models import Customers, NotificationCounters, Notifications
from django.http import HttpResponse
from django.views import View
import re, asyncio

class Service(View):

    " Get labels from the model" \
    " The cache are not implemented so the query is executed each time "
    def label_parsing(request):
        if request.method == 'POST':
            try:
                queryset = Customers.objects.values('notification_label', 'id')

                " truncate at 300 "
                notification = str(request.body)[:300] if len(str(request.body)) > 300 else str(request.body)

                LoggerService.set_log_level('info').log('Getting labels from customers table')

                matches_count = 0
                customers_id = 0
                for index, label in enumerate(queryset):
                    search = label['notification_label']
                    regex = r"("+search+")"
                    matches = re.findall(regex, notification, re.MULTILINE | re.IGNORECASE)
                    matches_count += len(matches)

                    if matches_count >= 1:
                        customers_id = label['id']
                    """ If there is more then one label, the customers object will be emptied """
                    if matches_count >= 2:
                        customers_id = 0

                LoggerService.set_log_level('debug').log('Matches: ' + str(matches_count) + ' - c_id: ' + str(customers_id))

                " Save notification if there is any matching"
                if matches_count >= 0:
                    Service.save_notification(notification, customers_id)

                return HttpResponse("Notification received!!", content_type="text/plain")

            except Exception as e:
                LoggerService.set_log_level('error').log(e)
                return HttpResponse("Error!!", content_type="text/plain")
        else:
            LoggerService.set_log_level('debug').log("Service.label_parsing different protocol received: " + request.method)
            return HttpResponse("Welcome!!", content_type="text/plain")

    " Actually we are not checking the data inserted into db, we assume it's safe"
    def save_notification(body, id_customer):
        notification = Notifications()
        notification.body = str(body)
        if id_customer != 0:
            notification.id_customer = id_customer
        try:
            notification.save()
        except Exception as e:
            LoggerService.set_log_level('error').log(e)

    def increment_notification_customer_counter(self):
        notificationCounters = NotificationCounters()