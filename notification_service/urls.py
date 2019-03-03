from django.urls import path

from .service import Service

urlpatterns = [
    path('notification/', Service.label_parsing),
]