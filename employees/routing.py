from django.urls import path
from .consumers import EmployeeConsumer

websocket_urlpatterns = [
    path("ws/employees/", EmployeeConsumer.as_asgi()),
]