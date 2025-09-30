# leafnoise API
Prueba técnica - Sistema de gestión de empleados, posiciones y tareas desarrollado con Django REST Framework y MongoDB.

## 🚀 Características

- **Gestión de Empleados**: CRUD completo con filtros y paginación
- **Gestión de Posiciones**: Administración de roles y cargos
- **Gestión de Tareas**: Sistema de tareas con estados y asignación
- **Reporte de Salario**: Análisis financiero para el CFO
- **API Documentada**: Swagger UI integrado
- **Base de Datos**: MongoDB con MongoEngine

## 🛠️ Tecnologías

- Django 5.2.6
- Django REST Framework 3.16.1
- MongoDB con MongoEngine
- Swagger/OpenAPI (drf-spectacular)

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- MongoDB
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd peopleFlow
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
DB_NAME=peopleflow
DB_HOST=localhost:27017
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_AUTH_SOURCE=admin
```

5. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor**
```bash
python manage.py runserver
```


## 📚 API Endpoints

### Empleados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/employees/` | Listar empleados |
| POST | `/api/employees/` | Crear empleado |
| GET | `/api/employees/{id}/` | Obtener empleado |
| PUT | `/api/employees/{id}/` | Actualizar empleado |
| DELETE | `/api/employees/{id}/` | Eliminar empleado |
| GET | `/api/employees/salary-report/` | Reporte de salarios |

### Posiciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/positions/` | Listar posiciones |
| POST | `/api/positions/` | Crear posición |
| GET | `/api/positions/{id}/` | Obtener posición |
| PUT | `/api/positions/{id}/` | Actualizar posición |
| DELETE | `/api/positions/{id}/` | Eliminar posición |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar tareas |
| POST | `/api/tasks/` | Crear tarea |
| GET | `/api/tasks/{id}/` | Obtener tarea |
| PUT | `/api/tasks/{id}/` | Actualizar tarea |
| DELETE | `/api/tasks/{id}/` | Eliminar tarea |
| PATCH | `/api/tasks/{id}/status/` | Actualizar estado de tarea |

## 🔍 Filtros y Paginación

### Empleados
- **Filtro por posición**: `?position=<position_id>`
- **Paginación**: `?page=<numero>&page_size=<tamaño>`
- **Ejemplo**: `/api/employees/?position=507f1f77bcf86cd799439011&page=1&page_size=10`

### Tareas
- **Filtro por empleado**: `?employee_id=<employee_id>`
- **Filtro por estado**: `?status=<status>`
- **Paginación**: `?page=<numero>&page_size=<tamaño>`
- **Estados disponibles**: `open`, `blocked`, `inprogress`, `qa`, `done`
- **Ejemplo**: `/api/tasks/?employee_id=507f1f77bcf86cd799439011&status=open&page=1&page_size=10`

## 📊 Reportes

### Reporte de Salarios
Endpoint: `GET /api/employees/salary-report/`

Incluye:
- Total de empleados
- Salario promedio
- Salario mínimo y máximo
- Total de salarios
- Fecha de generación

## 📖 Documentación

La documentación interactiva está disponible en:
- **Swagger UI**: `http://localhost:8000/api/docs/`

## 🗄️ Base de Datos

### Modelos

#### Empleado
- `name`: Nombre
- `last_name`: Apellido
- `email`: Email único
- `phone`: Teléfono
- `position`: Referencia a posición
- `salary`: Salario
- `hire_date`: Fecha de ingreso
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización
- `deleted_at`: Fecha de eliminación (soft delete)

#### Posición
- `name`: Nombre de la posición
- `description`: Descripción
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

#### Tarea
- `title`: Título de la tarea
- `description`: Descripción detallada
- `status`: Estado actual (open, blocked, inprogress, qa, done)
- `priority`: Prioridad (low, medium, high)
- `assigned_to`: Empleado asignado
- `created_by`: Empleado que creó la tarea
- `due_date`: Fecha límite
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización


## 🐳 Docker

### Docker Compose
```bash
docker-compose up -d
```

### Dockerfile
```bash
docker build -t peopleflow-api .
docker run -p 8000:8000 peopleflow-api
```

## 🧪 Testing

### Ejecutar tests
```bash
python manage.py test
```

### Ejemplo de request con curl

#### Registro
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Listar empleados
```bash
curl -X GET http://localhost:8000/api/employees/
```

#### Listar tareas
```bash
curl -X GET http://localhost:8000/api/tasks/
```

#### Crear tarea
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar nueva funcionalidad",
    "description": "Desarrollar la nueva característica solicitada",
    "priority": "high",
    "assigned_to": "507f1f77bcf86cd799439011",
    "created_by": "507f1f77bcf86cd799439012",
    "due_date": "2024-02-15T00:00:00Z"
  }'
```

#### Actualizar estado de tarea
```bash
curl -X PATCH http://localhost:8000/api/tasks/507f1f77bcf86cd799439011/status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "inprogress"
  }'
```

## 📝 Notas de Desarrollo

- **Soft Delete**: Los empleados eliminados se marcan con `deleted_at` en lugar de eliminarse físicamente
- **Validaciones**: Email único, salarios positivos, fechas válidas
- **Paginación**: Máximo 100 elementos por página
- **Filtros**: Búsqueda por posición y empleado con validación de ID
- **Estados de Tareas**: Sistema de estados con validación (open, blocked, inprogress, qa, done)
- **Asignación de Tareas**: Relación entre empleados y tareas

## 🚨 Troubleshooting

### Error de conexión a MongoDB
- Verificar que MongoDB esté ejecutándose
- Revisar las variables de entorno de conexión
- Comprobar credenciales de autenticación

### Error de validación de tareas
- Verificar que los IDs de empleados sean válidos
- Comprobar que el estado sea uno de los permitidos
- Asegurar que las fechas sean válidas


---

**Desarrollado Jimmy Sebastian Higa Ramirez**
