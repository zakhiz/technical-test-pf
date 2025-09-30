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

### 🐳 **Opción con Docker (Recomendado)**

1. **Levantar con Docker Compose**
```bash
docker-compose up --build
```

2. **Poblar la base de datos con datos de prueba**
```bash
docker-compose exec api python manage.py seed_data
```

3. **Acceder a la aplicación**
- **API**: `http://localhost:8000/api/`
- **Documentación**: `http://localhost:8000/api/docs/`


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
- `deleted`: Estado de eliminación (soft delete)
- `deleted_at`: Fecha de eliminación
- `replacement_employee`: Empleado que reemplaza al eliminado

#### Posición
- `name`: Nombre de la posición
- `description`: Descripción
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

#### Tarea
- `title`: Título de la tarea
- `description`: Descripción detallada
- `status`: Estado actual (open, blocked, inprogress, qa, done)
- `assigned_to`: Empleado asignado
- `due_date`: Fecha límite
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización
- `transferred_to`: Empleado al que se transfirió la tarea
- `transferred_at`: Fecha de transferencia


## 🐳 Docker

### Comandos Docker

#### Levantar la aplicación
```bash
# Construir y levantar todos los servicios
docker-compose up --build

# Levantar en segundo plano
docker-compose up -d --build
```

#### Poblar datos de prueba
```bash
# Ejecutar seed data
docker-compose exec api python manage.py seed_data
```

#### Comandos útiles
```bash
# Ver logs
docker-compose logs -f api

# Acceder al contenedor
docker-compose exec api bash

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down
```

#### Construir imagen individual
```bash
docker build -t peopleflow-api .
docker run -p 8000:8000 peopleflow-api
```

### Ejemplo de request con curl


#### Listar empleados
```bash
curl -X GET http://localhost:8000/api/employees/
```

#### Listar posiciones
```bash
curl -X GET http://localhost:8000/api/positions/
```

#### Listar tareas
```bash
curl -X GET http://localhost:8000/api/tasks/
```

#### Crear empleado
```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@company.com",
    "phone": "1234567890",
    "position": "507f1f77bcf86cd799439011",
    "salary": 75000.00,
    "hire_date": "2024-01-15T00:00:00Z"
  }'
```

#### Crear tarea
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar nueva funcionalidad",
    "description": "Desarrollar la nueva característica solicitada",
    "assigned_to": "507f1f77bcf86cd799439011",
    "status": "open",
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

## 🎯 Analisis del caso presentado

### Solucion propuesta para las problematicas encontradas

**Problemas detectados**
- Datos duplicados
- Errores de tipeo y problemas al detectar estos
- Baja productividad al momento de navegar o querer buscar algo simple

**Ecosistema Empleados, posiciones, tareas**

**Soluciones para probar y tomar en cuenta**

- **Modulo de posiciones / roles**: division de datos para evitar que exista problemas de tipados en la posicion / rol del empleado se genero una colleccion aparte para manejar esto.

- **Modulo de tareas**: para llevar el control del trabajo diario, semanal y mensual.

- **Modulo de empleados**: alta de empleados, asignacion de puesto / rol por medio del id del puesto, salario, datos personales del empleado y por ultimo no menos importante se agrego un sistema de desactivacion de empleados el cual busca que no se elimine desde un inicio el usuario sino que se deshabilita y se debe reemplazar por otro empleado activo al cual se le asignan todas sus tareas que tenga asignadas el empleado deshabilitado.

- **Funcion de reporte**: Nacho podra ver en el reporte la cantidad de empleados, media de salarios, salarios minimos, salarios maximos, y el total de todos los salarios.

**Modulo de reportes (tarea proxima pensada):**

- **Reporte de sueldos semanales**. (la idea era solicitar el reporte por medio de un cron job el cual se configuraria para todos los lunes, a la misma hora y que este le muestre los siguientes datos la cantidad de empleados, media de salarios, salarios minimos, salarios maximos, y el total de todos los salarios. ademas de esto pense crear un grafico el cual pueda dejar en claro los picos de los sueldos, cantidad de empleados con tal cantidades de sueldos. no llegue con el tiempo :c mil disculpas!)

## 📝 Notas de Desarrollo

### **🗑️ Sistema de Soft Delete**
- **Empleados eliminados**: Se marcan con `deleted=True` y `deleted_at`
- **NO se eliminan físicamente**: Se mantiene el historial completo
- **Reemplazo obligatorio**: Al eliminar empleado, se debe especificar `replacement_employee_id`
- **Transferencia automática**: Las tareas se transfieren al empleado de reemplazo

### **🔄 Transferencia de Tareas**
- **Automática**: Al eliminar empleado, todas sus tareas se transfieren
- **Historial**: Se registra `transferred_to` y `transferred_at` en cada tarea
- **Integridad**: No se pierden tareas en el proceso de eliminación

### **✅ Validaciones y Reglas**
- **Email único**: No se permiten emails duplicados en empleados
- **Salarios positivos**: Validación de salarios mayores a 0
- **Fechas válidas**: Validación de fechas de ingreso y vencimiento
- **Estados de tareas**: Solo estados válidos (open, blocked, inprogress, qa, done)
- **Paginación**: Máximo 100 elementos por página
- **Filtros**: Búsqueda por posición y empleado con validación de ID


**Desarrollado por Jimmy Sebastian Higa Ramirez**
