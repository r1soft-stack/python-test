from django.db import models


class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    notification_label = models.CharField(max_length=50, unique=True)


class NotificationCounters(models.Model):
    class Meta:
        unique_together = (('id', 'day'),)

    id = models.IntegerField(primary_key=True)
    num = models.IntegerField(default='0')
    day = models.DateField()
    id_customers = models.ForeignKey('Customers', on_delete='cascade')


# Notifications id is auto created
class Notifications(models.Model):
    body = models.TextField(null=False)
    id_customer = models.ForeignKey('Customers', on_delete='cascade', null=True)
