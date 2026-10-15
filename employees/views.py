import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Employee
from .forms import EmployeeForm
from employees.decorators.audit_log import log_view_action 
from django.db import DatabaseError
from django.contrib import messages
from employees.services.employee_service import EmployeeService
from employees.notifications import broadcast
from django.core.cache import cache
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)
# Create your views here.

@login_required
def index(request):
    employees = Employee.objects.all()

    q = request.GET.get('q', '').strip()
    department = request.GET.get('department', '')
    emp_type = request.GET.get('employment_type', '')
    status = request.GET.get('status', '')

    if q:
        employees = employees.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(employee_id__icontains=q)
        )
    if department:
        employees = employees.filter(department=department)
    if emp_type:
        employees = employees.filter(employment_type=emp_type)
    if status == 'active':
        employees = employees.filter(is_active=True)
    elif status == 'inactive':
        employees = employees.filter(is_active=False)

    return render(request, 'employees/index.html', {
        'employees': employees,
        'department_choices': Employee.DEPARTMENT_CHOICES,
        'employment_type_choices': Employee.EMPLOYMENT_TYPE_CHOICES,
        'q': q,
        'selected_department': department,
        'selected_type': emp_type,
        'selected_status': status,
        'stats': EmployeeService().get_card_statistics(),
    })

@login_required
def view_employee(request, id):
    employee = Employee.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

@login_required
@log_view_action
def add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            new_employee_id = form.cleaned_data['employee_id']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_phone = form.cleaned_data['phone']
            new_department = form.cleaned_data['department']
            new_job_title = form.cleaned_data['job_title']
            new_employment_type = form.cleaned_data['employment_type']
            new_hire_date = form.cleaned_data['hire_date']
            new_salary = form.cleaned_data['salary']
            new_is_active = form.cleaned_data['is_active']

            new_employee = Employee(
                employee_id = new_employee_id,
                first_name = new_first_name,
                last_name = new_last_name,
                email = new_email,
                phone = new_phone,
                department = new_department,
                job_title = new_job_title,
                employment_type = new_employment_type,
                hire_date = new_hire_date,
                salary = new_salary,
                is_active = new_is_active 
            )
            new_employee.save()
            cache.delete('card_stats')
            broadcast(f"{new_employee.first_name} {new_employee.last_name} was added by {request.user.username}")
            return render(request, 'employees/add.html',{
                'form' : form,
                'success' : True
            })
    else:
        form = EmployeeForm()
    return render(request, 'employees/add.html', {
        'form' : EmployeeForm()
    })

@login_required
@log_view_action
def edit(request, id):
    if request.method =='POST':
        employee = Employee.objects.get(pk=id)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            cache.delete('card_stats')
            return render(request, 'employees/edit.html', {
                'form' : form,
                'success' : True
            })
    else:
        employee = Employee.objects.get(pk=id)
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit.html', {
        'form' : form
    })

@login_required
@log_view_action
def delete(request, id):
    if request.method == 'POST':
        employee = Employee.objects.get(pk=id)
        request.session['deleted_name'] = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        cache.delete('card_stats')
        broadcast(f"{request.session['deleted_name']} was deleted by {request.user.username}. Please refresh the page.")
        return HttpResponseRedirect(reverse('delete_success'))
    return HttpResponseRedirect(reverse('index'))

@login_required
@log_view_action
def delete_success(request):
    name = request.session.pop('deleted_name', None)
    return render(request, 'employees/delete_success.html', {'name': name})

def landing(request):
    return render(request, 'employees/landing.html')

@login_required
def clear_cache(request):
    cache.clear()
    return HttpResponse("Cache cleared successfully")

@login_required
def detail(request, id):
    employee = get_object_or_404(Employee, pk=id)
    recent = request.session.get('recently_viewed', [])
    recent = [r for r in recent if r['id'] != employee.id]
    recent.insert(0, {'id': employee.id, 'name': f"{employee.first_name} {employee.last_name}"})
    request.session['recently_viewed'] = recent[:5]
    return render(request, 'employees/detail.html', {
        'employee': employee,
        'recently_viewed': request.session['recently_viewed'],
    })