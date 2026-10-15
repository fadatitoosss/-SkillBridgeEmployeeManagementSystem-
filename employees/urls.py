from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>',views.view_employee, name='view_employee'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('', views.landing, name='landing'),
    path('employees/', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='employees/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('deleted/', views.delete_success, name='delete_success'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
    path('employee/<int:id>/', views.detail, name='detail'),
    # path('api/search/', views.employee_search_ajax, name='employee_search_ajax'),
]
