from employees.repositories.employee_repository import EmployeeRepository

def __init__(self, repository: EmployeeRepository = None):
    self.repository = repository or EmployeeRepository()
