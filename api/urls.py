from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.employee_list, name="api_employee_list"),
    path("employees/<int:pk>/", views.employee_detail, name="api_employee_detail"),
]