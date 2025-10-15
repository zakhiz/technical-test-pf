from django.core.management.base import BaseCommand
from apps.positions.models import Position
from apps.employees.models import Employee
from apps.tasks.models import Task
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **options):
        self.create_positions()
        self.create_employees()
        self.create_tasks()
        self.stdout.write('Seed executed successfully')

    def create_positions(self):
        positions_data = [
            {'name': 'CEO', 'description': 'Chief Executive Officer'},
            {'name': 'CTO', 'description': 'Chief Technology Officer'},
            {'name': 'CFO', 'description': 'Chief Financial Officer'},
            {'name': 'Developer', 'description': 'Software Developer'},
            {'name': 'Designer', 'description': 'UI/UX Designer'},
            {'name': 'Manager', 'description': 'Project Manager'},
            {'name': 'Analyst', 'description': 'Business Analyst'},
            {'name': 'QA', 'description': 'Quality Assurance'},
            {'name': 'DevOps', 'description': 'DevOps Engineer'},
            {'name': 'HR', 'description': 'Human Resources'}
        ]

        for pos_data in positions_data:
            try:
                position = Position.objects.get(name=pos_data['name'])
                self.stdout.write(
                    f'Position already exists: {pos_data["name"]}')
            except Position.DoesNotExist:
                position = Position(
                    name=pos_data['name'],
                    description=pos_data['description'],
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                position.save()
                self.stdout.write(f'Created position: {pos_data["name"]}')

    def create_employees(self):

        employees_data = [
            {'name': 'Juan', 'last_name': 'Pérez',
                'email': 'juan.perez@company.com', 'position': 'CEO'},
            {'name': 'María', 'last_name': 'González',
                'email': 'maria.gonzalez@company.com', 'position': 'CTO'},
            {'name': 'Carlos', 'last_name': 'López',
                'email': 'carlos.lopez@company.com', 'position': 'CFO'},
            {'name': 'Ana', 'last_name': 'Martín',
                'email': 'ana.martin@company.com', 'position': 'Developer'},
            {'name': 'Luis', 'last_name': 'Rodríguez',
                'email': 'luis.rodriguez@company.com', 'position': 'Developer'},
            {'name': 'Sofia', 'last_name': 'Hernández',
                'email': 'sofia.hernandez@company.com', 'position': 'Designer'},
            {'name': 'Diego', 'last_name': 'García',
                'email': 'diego.garcia@company.com', 'position': 'Manager'},
            {'name': 'Laura', 'last_name': 'Fernández',
                'email': 'laura.fernandez@company.com', 'position': 'Analyst'},
            {'name': 'Miguel', 'last_name': 'Sánchez',
                'email': 'miguel.sanchez@company.com', 'position': 'QA'},
            {'name': 'Elena', 'last_name': 'Ramírez',
                'email': 'elena.ramirez@company.com', 'position': 'DevOps'},
            {'name': 'Roberto', 'last_name': 'Jiménez',
                'email': 'roberto.jimenez@company.com', 'position': 'HR'},
            {'name': 'Carmen', 'last_name': 'Torres',
                'email': 'carmen.torres@company.com', 'position': 'Developer'},
            {'name': 'Pablo', 'last_name': 'Díaz',
                'email': 'pablo.diaz@company.com', 'position': 'Designer'},
            {'name': 'Isabel', 'last_name': 'Moreno',
                'email': 'isabel.moreno@company.com', 'position': 'Manager'},
            {'name': 'Antonio', 'last_name': 'Álvarez',
                'email': 'antonio.alvarez@company.com', 'position': 'Analyst'}
        ]

        for emp_data in employees_data:
            try:
                position = Position.objects.get(name=emp_data['position'])
                try:
                    employee = Employee.objects.get(email=emp_data['email'])
                    self.stdout.write(
                        f'Employee already exists: {emp_data["name"]} {emp_data["last_name"]}')
                except Employee.DoesNotExist:
                    employee = Employee(
                        name=emp_data['name'],
                        last_name=emp_data['last_name'],
                        email=emp_data['email'],
                        position=position,
                        salary=random.randint(30000, 120000),
                        phone=f'555-{random.randint(1000, 9999)}',
                        hire_date=datetime.now(),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    employee.save()
                    self.stdout.write(
                        f'Created employee: {emp_data["name"]} {emp_data["last_name"]}')
            except Position.DoesNotExist:
                self.stdout.write(
                    f'Position not found: {emp_data["position"]}')

    def create_tasks(self):
        employees = list(Employee.objects.all())

        tasks_data = [
            {'title': 'Implementar autenticación',
                'description': 'Desarrollar sistema de login y registro', 'status': 'open'},
            {'title': 'Diseñar dashboard principal',
                'description': 'Crear interfaz del dashboard principal', 'status': 'inprogress'},
            {'title': 'Configurar base de datos',
                'description': 'Configurar MongoDB y conexiones', 'status': 'done'},
            {'title': 'Revisar código de seguridad',
                'description': 'Auditoría de seguridad del código', 'status': 'qa'},
            {'title': 'Optimizar rendimiento',
                'description': 'Mejorar velocidad de la aplicación', 'status': 'blocked'},
            {'title': 'Crear documentación API',
                'description': 'Documentar todos los endpoints', 'status': 'open'},
            {'title': 'Implementar tests unitarios',
                'description': 'Añadir tests para módulos críticos', 'status': 'inprogress'},
            {'title': 'Configurar CI/CD',
                'description': 'Automatizar despliegues', 'status': 'open'},
            {'title': 'Revisar UX/UI',
                'description': 'Evaluar experiencia de usuario', 'status': 'qa'},
            {'title': 'Migrar datos legacy',
                'description': 'Migrar datos del sistema anterior', 'status': 'blocked'},
            {'title': 'Implementar notificaciones',
                'description': 'Sistema de notificaciones push', 'status': 'open'},
            {'title': 'Crear reportes financieros',
                'description': 'Generar reportes automáticos', 'status': 'inprogress'},
            {'title': 'Configurar monitoreo',
                'description': 'Implementar sistema de monitoreo', 'status': 'open'},
            {'title': 'Revisar accesibilidad',
                'description': 'Auditar accesibilidad web', 'status': 'qa'},
            {'title': 'Implementar backup',
                'description': 'Sistema de respaldo automático', 'status': 'done'},
            {'title': 'Optimizar consultas DB',
                'description': 'Mejorar rendimiento de consultas', 'status': 'inprogress'},
            {'title': 'Crear guías de usuario',
                'description': 'Documentación para usuarios finales', 'status': 'open'},
            {'title': 'Implementar caché',
                'description': 'Sistema de caché para mejor rendimiento', 'status': 'blocked'},
            {'title': 'Revisar compliance',
                'description': 'Verificar cumplimiento normativo', 'status': 'qa'},
            {'title': 'Configurar logs',
                'description': 'Sistema de logging centralizado', 'status': 'done'}
        ]

        for task_data in tasks_data:
            if employees:  # Verificar que hay empleados disponibles
                assigned_employee = random.choice(employees)
                due_date = datetime.now() + timedelta(days=random.randint(1, 30))

                try:
                    task = Task.objects.get(
                        title=task_data['title'], assigned_to=assigned_employee)
                    self.stdout.write(
                        f'Task already exists: {task_data["title"]}')
                except Task.DoesNotExist:
                    task = Task(
                        title=task_data['title'],
                        assigned_to=assigned_employee,
                        description=task_data['description'],
                        status=task_data['status'],
                        due_date=due_date,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    task.save()
                    self.stdout.write(f'Created task: {task_data["title"]}')
            else:
                self.stdout.write('No employees available to assign tasks')
