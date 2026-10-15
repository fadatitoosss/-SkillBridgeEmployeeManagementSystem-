from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from employees.models import Employee

# Create your views here.
def serialize(e):
    return {
        "id": e.id,
        "employee_id": e.employee_id,
        "first_name": e.first_name,
        "last_name": e.last_name,
        "email": e.email,
        "department": e.get_department_display(),
        "job_title": e.job_title,
        "employment_type": e.get_employment_type_display(),
        "hire_date": e.hire_date.isoformat(),
        "is_active": e.is_active,
    }


@require_GET
def employee_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    employees = Employee.objects.all()

    search = request.GET.get("search")
    if search:
        employees = employees.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
        )

    department = request.GET.get("department")
    if department:
        employees = employees.filter(department=department)

    return JsonResponse([serialize(e) for e in employees], safe=False)


@require_GET
def employee_detail(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)

    return JsonResponse(serialize(employee))