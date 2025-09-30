from ..serializer import TaskSerializer
from ..models import Task
from apps.employees.models import Employee
from bson import ObjectId
from datetime import datetime


class TaskService:
    @staticmethod
    def get_all_tasks():
        try:
            tasks = Task.objects()
            return tasks, None
        except Exception as e:
            return None, f"Error getting all tasks: {e}"

    @staticmethod
    def get_tasks_by_employee(employee_id):
        try:
            tasks = Task.objects(assigned_to=ObjectId(employee_id))
            return tasks, None
        except Exception as e:
            return None, f"Error getting tasks for employee: {e}"

    @staticmethod
    def get_task_by_id(task_id):
        try:
            task = Task.objects.get(id=task_id)
            return task, None
        except Task.DoesNotExist:
            return None, "Task not found"
        except Exception as e:
            return None, f"Error getting task by id: {e}"

    @staticmethod
    def create_task(data):
        try:
            assigned_to_id = data.get('assigned_to')
            if assigned_to_id:
                try:
                    Employee.objects.get(id=assigned_to_id, deleted=False)
                except Employee.DoesNotExist:
                    raise ValueError(
                        f"Employee with ID '{assigned_to_id}' does not exist or is deleted")

            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                task = serializer.save()
                return task, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error creating task: {str(e)}"

    @staticmethod
    def update_task(task, data):
        try:
            assigned_to_id = data.get('assigned_to')
            if assigned_to_id:
                try:
                    Employee.objects.get(id=assigned_to_id, deleted=False)
                except Employee.DoesNotExist:
                    raise ValueError(
                        f"Employee with ID '{assigned_to_id}' does not exist or is deleted")

            serializer = TaskSerializer(task, data=data, partial=True)
            if serializer.is_valid():
                updated_task = serializer.save()
                return updated_task, None
            return None, serializer.errors
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error updating task: {str(e)}"

    @staticmethod
    def delete_task(task):
        try:
            task.delete()
            return True, None
        except Exception as e:
            return False, f"Error deleting task: {str(e)}"

    @staticmethod
    def transfer_tasks_from_employee(employee_id, new_employee_id):

        try:
            try:
                Employee.objects.get(id=employee_id)
                new_employee = Employee.objects.get(
                    id=new_employee_id, deleted=False)
            except Employee.DoesNotExist:
                raise ValueError(
                    "One or both employees do not exist or are deleted")

            tasks = Task.objects(assigned_to=ObjectId(employee_id))

            transferred_count = 0
            for task in tasks:
                task.assigned_to = new_employee
                task.transferred_to = new_employee
                task.transferred_at = datetime.now()
                task.save()
                transferred_count += 1

            return transferred_count, None
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Error transferring tasks: {str(e)}"
