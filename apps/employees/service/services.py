from ..serializer import EmployeeSerializer
from apps.common.constants import ERROR_MESSAGES
from ..models import Employee
from decimal import Decimal
from bson import ObjectId
from apps.positions.models import Position


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
                try:
                    query['position'] = ObjectId(position_filter)
                except Exception as e:
                    return None, f"Invalid position ID format: {e}"

            total = Employee.objects(**query).count()
            total_pages = (total + page_size - 1) // page_size

            offset = (page - 1) * page_size

            employees = Employee.objects(**query).skip(offset).limit(page_size)

            employees_with_position = []
            for employee in employees:
                position_name = EmployeeService._get_position_name(
                    employee.position)
                employee_data = {
                    'employee': employee,
                    'position_name': position_name
                }
                employees_with_position.append(employee_data)

            return {
                'data': employees_with_position,
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
            email = data.get('email')
            if email and Employee.objects(email=email).first():
                raise ValueError(
                    f"Employee with email '{email}' already exists")

            position_id = data.get('position')
            if position_id:
                try:
                    Position.objects.get(id=position_id)
                except Position.DoesNotExist:
                    raise ValueError(
                        f"Position with ID '{position_id}' does not exist")

            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                employee = serializer.save()
                return employee, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error creating employee: {str(e)}"

    @staticmethod
    def update_employee(employee, data):
        try:
            email = data.get('email')
            if email and email != employee.email:
                existing_employee = Employee.objects(email=email).first()
                if existing_employee and existing_employee.id != employee.id:
                    raise ValueError(
                        f"Employee with email '{email}' already exists")

            position_id = data.get('position')
            if position_id:
                try:
                    Position.objects.get(id=position_id)
                except Position.DoesNotExist:
                    raise ValueError(
                        f"Position with ID '{position_id}' does not exist")

            serializer = EmployeeSerializer(employee, data=data, partial=True)
            if serializer.is_valid():
                updated_employee = serializer.save()
                return updated_employee, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
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
        try:

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

    @staticmethod
    def _get_position_name(position):

        if not position:
            raise ValueError("Employee has no position assigned")

        try:
            position_obj = Position.objects.get(id=position.id)
            if not position_obj.name:
                raise ValueError(
                    f"Position {position.id} exists but has no name")
            return position_obj.name
        except Position.DoesNotExist:
            raise ValueError(
                f"Position with ID {position.id} does not exist in database")
        except Exception as e:
            raise ValueError(
                f"Error accessing position {position.id}: {str(e)}")
