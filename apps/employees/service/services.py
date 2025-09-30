from ..serializer import EmployeeSerializer
from apps.common.constants import ERROR_MESSAGES
from ..models import Employee


class EmployeeService:
    @staticmethod
    def get_all_employees():
        try:
            employees = Employee.objects.all()
            return employees, None
        except Exception as e:
            return None, f"Error getting all employees: {e}"

    @staticmethod
    def get_employees_with_filters(position_filter=None, page=1, page_size=10):
        try:
            query = {}
            if position_filter:
                from bson import ObjectId
                try:
                    query['position'] = ObjectId(position_filter)
                except Exception as e:
                    return None, f"Invalid position ID format: {e}"

            total = Employee.objects(**query).count()
            total_pages = (total + page_size - 1) // page_size

            offset = (page - 1) * page_size

            employees = Employee.objects(**query).skip(offset).limit(page_size)

            return {
                'data': employees,
                'total': total,
                'total_pages': total_pages
            }, None
        except Exception as e:
            return None, f"Error getting employees with filters: {e}"

    @staticmethod
    def get_employee_by_id(employee_id):
        try:
            employee = Employee.objects.get(
                id=employee_id)
            return employee, None
        except Employee.DoesNotExist:
            return None, ERROR_MESSAGES['employee']['not_found']
        except Exception as e:
            return None, f"Error getting employee by id: {e}"

    @staticmethod
    def create_employee(data):
        try:
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                employee = serializer.save()
                return employee, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error creating employee: {str(e)}"

    @staticmethod
    def update_employee(employee, data):
        try:
            serializer = EmployeeSerializer(employee, data=data, partial=True)
            if serializer.is_valid():
                updated_employee = serializer.save()
                return updated_employee, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error updating employee: {str(e)}"

    @staticmethod
    def delete_employee(employee):
        try:
            employee.delete()
            return True, None
        except Exception as e:
            return False, f"Error deleting employee: {str(e)}"

    @staticmethod
    def get_employee_by_email(email):
        try:
            employee = Employee.objects.get(email=email)
            return employee, None
        except Employee.DoesNotExist:
            return None, ERROR_MESSAGES['employee']['not_found']
        except Exception as e:
            return None, f"Error getting employee by email: {str(e)}"

    @staticmethod
    def get_employee_by_position(position):
        try:
            employees = Employee.objects.filter(position=position)
            return employees, None
        except Exception as e:
            return None, f"Error getting employees by position: {str(e)}"

    @staticmethod
    def get_employees_by_salary(salary):
        try:
            employees = Employee.objects.filter(
                salary=salary)
            return employees, None
        except Exception as e:
            return None, f"Error getting employees by salary: {str(e)}"

    @staticmethod
    def get_salary_report():
        """
        """
        try:
            from decimal import Decimal

            employees = Employee.objects.all()

            if not employees:
                return {
                    'total_employees': 0,
                    'average_salary': 0,
                    'min_salary': 0,
                    'max_salary': 0,
                    'total_salary': 0
                }, None

            salaries = [float(emp.salary) for emp in employees]
            total_salary = sum(salaries)
            average_salary = total_salary / len(salaries)
            min_salary = min(salaries)
            max_salary = max(salaries)

            return {
                'total_employees': len(employees),
                'average_salary': round(average_salary, 2),
                'min_salary': min_salary,
                'max_salary': max_salary,
                'total_salary': total_salary,
                'generated_at': employees[0].created_at if employees else None
            }, None

        except Exception as e:
            return None, f"Error generating salary report: {e}"
