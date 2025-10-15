from http import HTTPStatus
from ..serializer import EmployeeSerializer
from apps.common.constants import ERROR_MESSAGES
from ..models import Employee
from decimal import Decimal
from bson import ObjectId
from apps.positions.models import Position
from apps.tasks.service import TaskService
from datetime import datetime

from apps.tasks.models import Task


class EmployeeService:
    @staticmethod
    def get_employees_with_filters(filters=None, page=1, page_size=10):
        try:
            if page < 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10

            query = {}

            if filters:
                if filters.get('name'):
                    query['name__icontains'] = filters['name']
                if filters.get('email'):
                    query['email__icontains'] = filters['email']

            total = Employee.objects(**query).count()
            total_pages = (total + page_size - 1) // page_size
            offset = (page - 1) * page_size

            employees = Employee.objects(**query).skip(offset).limit(page_size)
            employees_with_position = []

            for employee in employees:
                position_name = EmployeeService._get_position_name(
                    employee.position)
                employee_data = {
                    'id': str(employee.id),
                    'name': employee.name,
                    'last_name': employee.last_name,
                    'email': employee.email,
                    'phone': employee.phone,
                    'position': str(employee.position.id),
                    'salary': employee.salary,
                    'hire_date': employee.hire_date,
                    'position_name': position_name,
                    'deleted': employee.deleted,
                    'deleted_at': employee.deleted_at,
                    'replacement_employee': str(employee.replacement_employee.id) if employee.replacement_employee else None,
                }
                employees_with_position.append(employee_data)
            return {
                'success': True,
                'message': 'Employees fetched successfully',
                'data': employees_with_position,
                'total_employees': total,
                'total_pages': total_pages,
                'current_page': page,
            }, None
        except Exception as e:
            return None, f"Error getting employees with filters: {e}"

    @staticmethod
    def get_employee_by_id(employee_id):
        try:
            employee = Employee.objects.get(
                id=employee_id)
            serializer = EmployeeSerializer(employee)
            payload = {
                "success": True,
                "message": "Employee fetched successfully",
                "data": serializer.data
            }
            return payload, None
        except Employee.DoesNotExist:
            return None, ERROR_MESSAGES['employee']['not_found']
        except Exception as e:
            return None, f"Error getting employee by id: {e}"

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

            salaries = [emp.salary for emp in employees]
            total_salary = sum(salaries)
            average_salary = total_salary / len(salaries)
            min_salary = min(salaries)
            max_salary = max(salaries)

            return {
                'success': True,
                'message': 'Salary report generated successfully',
                'data': {
                    'total_employees': len(employees),
                    'average_salary': round(average_salary, 2),
                    'min_salary': min_salary,
                    'max_salary': max_salary,
                    'total_salary': total_salary,
                    'generated_at': datetime.now()
                }
            }, None

        except Exception as e:
            return None, f"Error generating salary report: {e}"

    @staticmethod
    def create_employee(data):
        try:
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                new_employee = serializer.save()
                if not new_employee:
                    raise ValueError("Employee not created")

                payload = {
                    "success": True,
                    "message": "Employee created successfully",
                    "data": {
                        "id": str(new_employee.id),
                    }
                }
                return payload, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error creating employee: {str(e)}"

    @staticmethod
    def update_employee(pk, data):
        try:
            employee = Employee.objects.get(
                id=pk)
            email = data.get('email')
            if email and email != employee.email:
                existing_employee = Employee.objects(email=email).first()
                if existing_employee and existing_employee.id != employee.id:
                    raise ValueError(
                        f"Employee with email '{email}' already exists")
            serializer = EmployeeSerializer(employee, data=data, partial=True)
            if serializer.is_valid():

                updated_employee = serializer.save()

                payload = {
                    "success": True,
                    "message": "Employee updated successfully",
                    "data": {
                        "id": str(updated_employee.id),
                    }
                }
                return payload, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error updating employee: {str(e)}"

    @staticmethod
    def delete_employee(employee, replacement_employee_id):
        try:

            tasks = Task.objects(assigned_to=employee)

            if tasks:
                try:
                    replacement_employee = Employee.objects.get(
                        id=replacement_employee_id, deleted=False
                    )
                except Employee.DoesNotExist:
                    return False, f"Replacement employee with ID '{replacement_employee_id}' does not exist or is deleted"

                transferred_count, error = TaskService.transfer_tasks_from_employee(
                    str(employee.id), replacement_employee_id
                )

                if error:
                    return False, f"Error transferring tasks: {error}"

                employee.deleted = True
                employee.deleted_at = datetime.now()
                employee.replacement_employee = replacement_employee
                employee.save()

                return True, None
            else:
                employee.deleted = True
                employee.deleted_at = datetime.now()
                employee.save()

                return True, None

        except Exception as e:
            return False, f"Error deleting employee: {str(e)}"
