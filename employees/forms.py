from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].initial = '+27'

    class Meta:
        model = Employee
        fields = [ 'employee_id', 'first_name', 'last_name', 'email', 'phone', 'department', 'job_title', 'employment_type', 'hire_date', 'salary', 'is_active']
        labels = {
            'employee_id':'Employee ID',
            'first_name' : 'First Name', 
            'last_name' : 'Last Name', 
            'email' : 'Email', 
            'phone' : 'Phone', 
            'department' : 'Department', 
            'job_title' : 'Job Title', 
            'employment_type' : 'Employment Type', 
            'hire_date' : 'Date Hired', 
            'salary' : 'Salary', 
            'is_active': "Is Active"
        }
        widgets ={
            'employee_id' : forms.TextInput(attrs={'class': 'form-control'}), 
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}), 
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}), 
            'email' : forms.EmailInput(attrs={'class': 'form-control'}), 
            'phone' : forms.TextInput(attrs={'class': 'form-control'}), 
            'department' : forms.Select(attrs={'class': 'form-select'}), 
            'job_title' : forms.TextInput(attrs={'class': 'form-control'}), 
            'employment_type' : forms.Select(attrs={'class': 'form-select'}), 
            'hire_date' :  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},format='%Y-%m-%d',), 
            'salary' : forms.NumberInput(attrs={'class': 'form-control'}), 
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }