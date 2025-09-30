from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


def employee_list_schema():
    return extend_schema(
        operation_id="list_employees",
        summary="Listar empleados",
        description="""
        Obtiene una lista paginada de empleados con filtros opcionales.
        
        **Filtros disponibles:**
        - `position`: Filtrar por ID de posición
        - `page`: Número de página (por defecto: 1)
        - `page_size`: Tamaño de página (por defecto: 10, máximo: 100)
        
        **Ejemplo de uso:**
        ```
        GET /api/employees/?position=507f1f77bcf86cd799439011&page=1&page_size=10
        ```
        """,
        tags=["Empleados"],
        parameters=[
            OpenApiParameter(
                name='position',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='ID de la posición para filtrar empleados',
                examples=[
                    OpenApiExample(
                        'Desarrollador',
                        value='507f1f77bcf86cd799439011',
                        description='Filtrar por posición de Desarrollador'
                    )
                ]
            ),
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Número de página',
                examples=[
                    OpenApiExample('Página 1', value=1),
                    OpenApiExample('Página 2', value=2)
                ]
            ),
            OpenApiParameter(
                name='page_size',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Tamaño de página (máximo 100)',
                examples=[
                    OpenApiExample('10 empleados', value=10),
                    OpenApiExample('25 empleados', value=25)
                ]
            )
        ],
        responses={
            200: OpenApiExample(
                'Lista de empleados exitosa',
                value={
                    "data": [
                        {
                            "id": "507f1f77bcf86cd799439011",
                            "name": "Juan",
                            "last_name": "Pérez",
                            "email": "juan.perez@company.com",
                            "phone": "1234567890",
                            "position": "507f1f77bcf86cd799439012",
                            "position_name": "Desarrollador Senior",
                            "salary": 75000.00,
                            "hire_date": "2024-01-15T00:00:00Z",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "page_size": 10,
                        "total": 25,
                        "total_pages": 3
                    }
                }
            ),
            500: OpenApiExample(
                'Error del servidor',
                value={"error": "Error interno del servidor"}
            )
        }
    )


def employee_create_schema():
    return extend_schema(
        operation_id="create_employee",
        summary="Crear empleado",
        description="""
        Crea un nuevo empleado en el sistema.
        
        **Campos requeridos:**
        - `name`: Nombre del empleado
        - `last_name`: Apellido del empleado
        - `email`: Email único del empleado
        - `phone`: Teléfono del empleado
        - `position`: ID de la posición
        - `salary`: Salario del empleado
        - `hire_date`: Fecha de ingreso (formato ISO 8601)
        
        **Validaciones:**
        - Email debe ser único
        - Position ID debe ser válido
        - Salary debe ser mayor a 0
        - Hire date no puede ser en el futuro
        """,
        tags=["Empleados"],
        responses={
            201: OpenApiExample(
                'Empleado creado exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "name": "María",
                    "last_name": "González",
                    "email": "maria.gonzalez@company.com",
                    "phone": "0987654321",
                    "position": "507f1f77bcf86cd799439012",
                    "position_name": "Desarrollador Senior",
                    "salary": 80000.00,
                    "hire_date": "2024-01-20T00:00:00Z",
                    "created_at": "2024-01-20T14:30:00Z",
                    "updated_at": "2024-01-20T14:30:00Z"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": {
                        "email": ["Email already exists"],
                        "salary": ["Salary cannot be negative"]
                    }
                }
            )
        },
        examples=[
            OpenApiExample(
                'Crear Desarrollador',
                value={
                    "name": "Carlos",
                    "last_name": "Rodríguez",
                    "email": "carlos.rodriguez@company.com",
                    "phone": "1122334455",
                    "position": "507f1f77bcf86cd799439012",
                    "salary": 65000.00,
                    "hire_date": "2024-01-25T00:00:00Z"
                },
                description='Ejemplo para crear un desarrollador'
            ),
            OpenApiExample(
                'Crear Manager',
                value={
                    "name": "Ana",
                    "last_name": "Martínez",
                    "email": "ana.martinez@company.com",
                    "phone": "5566778899",
                    "position": "507f1f77bcf86cd799439013",
                    "salary": 95000.00,
                    "hire_date": "2024-01-30T00:00:00Z"
                },
                description='Ejemplo para crear un manager'
            )
        ]
    )


def employee_detail_schema():
    return extend_schema(
        operation_id="get_employee",
        summary="Obtener empleado",
        description="Obtiene los detalles de un empleado específico por su ID",
        tags=["Empleados"],
        responses={
            200: OpenApiExample(
                'Empleado encontrado',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Juan",
                    "last_name": "Pérez",
                    "email": "juan.perez@company.com",
                    "phone": "1234567890",
                    "position": "507f1f77bcf86cd799439012",
                    "position_name": "Desarrollador Senior",
                    "salary": 75000.00,
                    "hire_date": "2024-01-15T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
                }
            ),
            404: OpenApiExample(
                'Empleado no encontrado',
                value={"error": "Empleado no encontrado"}
            )
        }
    )


def employee_update_schema():
    return extend_schema(
        operation_id="update_employee",
        summary="Actualizar empleado",
        description="Actualiza los datos de un empleado existente",
        tags=["Empleados"],
        responses={
            200: OpenApiExample(
                'Empleado actualizado exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Juan Carlos",
                    "last_name": "Pérez González",
                    "email": "juan.perez@company.com",
                    "phone": "1234567890",
                    "position": "507f1f77bcf86cd799439012",
                    "position_name": "Desarrollador Senior",
                    "salary": 80000.00,
                    "hire_date": "2024-01-15T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:30:00Z"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": {
                        "email": ["Email already exists"],
                        "salary": ["Salary cannot be negative"]
                    }
                }
            ),
            404: OpenApiExample(
                'Empleado no encontrado',
                value={"error": "Empleado no encontrado"}
            )
        }
    )


def employee_delete_schema():
    return extend_schema(
        operation_id="delete_employee",
        summary="Eliminar empleado",
        description="Elimina un empleado del sistema",
        tags=["Empleados"],
        responses={
            204: OpenApiExample(
                'Empleado eliminado exitosamente',
                value=None,
                description='No content - empleado eliminado'
            ),
            404: OpenApiExample(
                'Empleado no encontrado',
                value={"error": "Empleado no encontrado"}
            )
        }
    )


def salary_report_schema():
    return extend_schema(
        operation_id="get_salary_report",
        summary="Reporte de salarios",
        description="""
        Genera un reporte completo de salarios para el CFO.
        
        **Incluye:**
        - Total de empleados
        - Salario promedio
        - Salario mínimo y máximo
        - Total de salarios
        """,
        tags=["Reportes"],
        responses={
            200: OpenApiExample(
                'Reporte generado exitosamente',
                value={
                    "report": {
                        "total_employees": 25,
                        "average_salary": 75000.00,
                        "min_salary": 45000.00,
                        "max_salary": 120000.00,
                        "total_salary": 1875000.00,
                        "generated_at": "2024-01-20T14:30:00Z"
                    },
                    "message": "Salary report generated successfully",
                    "requested_by": "Nacho (CFO)",
                    "purpose": "Weekly budget planning"
                }
            ),
            500: OpenApiExample(
                'Error del servidor',
                value={"error": "Error interno del servidor"}
            )
        }
    )


def position_list_schema():
    return extend_schema(
        operation_id="list_positions",
        summary="Listar posiciones",
        description="Obtiene una lista de todas las posiciones disponibles",
        tags=["Posiciones"],
        responses={
            200: OpenApiExample(
                'Lista de posiciones exitosa',
                value=[
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "name": "Desarrollador Senior",
                        "description": "Desarrollo de software senior"
                    },
                    {
                        "id": "507f1f77bcf86cd799439012",
                        "name": "Manager",
                        "description": "Gestión de equipos"
                    }
                ]
            )
        }
    )


def position_create_schema():
    return extend_schema(
        operation_id="create_position",
        summary="Crear posición",
        description="Crea una nueva posición en el sistema",
        tags=["Posiciones"],
        responses={
            201: OpenApiExample(
                'Posición creada exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Desarrollador Junior",
                    "description": "Desarrollo de software junior"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": {
                        "name": ["Position with this name already exists"]
                    }
                }
            )
        }
    )


def task_list_schema():
    return extend_schema(
        operation_id="list_tasks",
        summary="Listar tareas",
        description="""
        Obtiene una lista paginada de tareas con filtros opcionales.
        
        **Filtros disponibles:**
        - `employee_id`: Filtrar por ID de empleado
        - `status`: Filtrar por estado (open, blocked, inprogress, qa, done)
        - `page`: Número de página (por defecto: 1)
        - `page_size`: Tamaño de página (por defecto: 10, máximo: 100)
        """,
        tags=["Tareas"],
        parameters=[
            OpenApiParameter(
                name='employee_id',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='ID del empleado para filtrar tareas'
            ),
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Estado de la tarea',
                examples=[
                    OpenApiExample('Abierta', value='open'),
                    OpenApiExample('En progreso', value='inprogress'),
                    OpenApiExample('Bloqueada', value='blocked'),
                    OpenApiExample('QA', value='qa'),
                    OpenApiExample('Completada', value='done')
                ]
            ),
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Número de página'
            ),
            OpenApiParameter(
                name='page_size',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Tamaño de página (máximo 100)'
            )
        ],
        responses={
            200: OpenApiExample(
                'Lista de tareas exitosa',
                value={
                    "data": [
                        {
                            "id": "507f1f77bcf86cd799439011",
                            "title": "Implementar autenticación",
                            "description": "Desarrollar sistema de login y registro",
                            "assigned_to": "507f1f77bcf86cd799439012",
                            "assigned_to_name": "Juan Pérez",
                            "status": "open",
                            "due_date": "2024-02-15T00:00:00Z",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "page_size": 10,
                        "total": 25,
                        "total_pages": 3
                    }
                }
            )
        }
    )


def task_create_schema():
    return extend_schema(
        operation_id="create_task",
        summary="Crear tarea",
        description="""
        Crea una nueva tarea en el sistema.
        
        **Campos requeridos:**
        - `title`: Título de la tarea
        - `assigned_to`: ID del empleado asignado
        
        **Campos opcionales:**
        - `description`: Descripción de la tarea
        - `status`: Estado de la tarea (por defecto: open)
        - `due_date`: Fecha de vencimiento
        """,
        tags=["Tareas"],
        responses={
            201: OpenApiExample(
                'Tarea creada exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "title": "Implementar autenticación",
                    "description": "Desarrollar sistema de login y registro",
                    "assigned_to": "507f1f77bcf86cd799439012",
                    "assigned_to_name": "Juan Pérez",
                    "status": "open",
                    "due_date": "2024-02-15T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": {
                        "title": ["This field is required"],
                        "assigned_to": ["Invalid employee ID"]
                    }
                }
            )
        }
    )


def task_detail_schema():
    return extend_schema(
        operation_id="get_task",
        summary="Obtener tarea",
        description="Obtiene los detalles de una tarea específica por su ID",
        tags=["Tareas"],
        responses={
            200: OpenApiExample(
                'Tarea encontrada',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "title": "Implementar autenticación",
                    "description": "Desarrollar sistema de login y registro",
                    "assigned_to": "507f1f77bcf86cd799439012",
                    "assigned_to_name": "Juan Pérez",
                    "status": "open",
                    "due_date": "2024-02-15T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
                }
            ),
            404: OpenApiExample(
                'Tarea no encontrada',
                value={"error": "Task not found"}
            )
        }
    )


def task_update_schema():
    return extend_schema(
        operation_id="update_task",
        summary="Actualizar tarea",
        description="Actualiza los datos de una tarea existente",
        tags=["Tareas"],
        responses={
            200: OpenApiExample(
                'Tarea actualizada exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "title": "Implementar autenticación v2",
                    "description": "Desarrollar sistema de login y registro mejorado",
                    "assigned_to": "507f1f77bcf86cd799439012",
                    "assigned_to_name": "Juan Pérez",
                    "status": "inprogress",
                    "due_date": "2024-02-20T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:30:00Z"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": {
                        "status": ["Invalid status. Must be one of: open, blocked, inprogress, qa, done"]
                    }
                }
            ),
            404: OpenApiExample(
                'Tarea no encontrada',
                value={"error": "Task not found"}
            )
        }
    )


def task_delete_schema():
    return extend_schema(
        operation_id="delete_task",
        summary="Eliminar tarea",
        description="Elimina una tarea del sistema",
        tags=["Tareas"],
        responses={
            200: OpenApiExample(
                'Tarea eliminada exitosamente',
                value={
                    "message": "Task deleted successfully"
                }
            ),
            404: OpenApiExample(
                'Tarea no encontrada',
                value={"error": "Task not found"}
            )
        }
    )


def task_status_update_schema():
    return extend_schema(
        operation_id="update_task_status",
        summary="Actualizar estado de tarea",
        description="Actualiza solo el estado de una tarea específica",
        tags=["Tareas"],
        responses={
            200: OpenApiExample(
                'Estado actualizado exitosamente',
                value={
                    "id": "507f1f77bcf86cd799439011",
                    "title": "Implementar autenticación",
                    "description": "Desarrollar sistema de login y registro",
                    "assigned_to": "507f1f77bcf86cd799439012",
                    "assigned_to_name": "Juan Pérez",
                    "status": "inprogress",
                    "due_date": "2024-02-15T00:00:00Z",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:30:00Z"
                }
            ),
            400: OpenApiExample(
                'Error de validación',
                value={
                    "error": "Invalid status. Must be one of: open, blocked, inprogress, qa, done"
                }
            ),
            404: OpenApiExample(
                'Tarea no encontrada',
                value={"error": "Task not found"}
            )
        }
    )
