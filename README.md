# OpsCenter
JORGE MARCILLO, EMILIO PUGA, PABLO GALARZA Y EDUARDO CEDEÑO
Plataforma interna de gestión de incidentes operativos para equipos fintech. Reemplaza el uso de correos, hojas de cálculo y mensajería informal con un sistema trazable, con roles, flujos de estado y notificaciones automáticas. OpsCenter centraliza el registro de incidentes, asignación de responsabilidad, y la gestión de notificaciones en una sola plataforma interna.

---

## Arquitectura

El proyecto sigue una **arquitectura hexagonal** (Ports & Adapters), con separación estricta entre capas:

```
opscenter/
├── backend/
│   ├── domain/          # Entidades, enums, reglas de negocio, interfaces de repositorio
│   │   ├── entities/    # User, Incident, Task, Notification
│   │   ├── enums/       # Role, Severity, IncidentStatus, TaskStatus, EventType
│   │   ├── states/      # Patrón State para el ciclo de vida de Incident
│   │   ├── commands/    # Patrón Command para envío de notificaciones
│   │   ├── templates/   # Patrón Template Method para construcción de mensajes
│   │   ├── observers/   # Patrón Observer / Event Bus
│   │   └── repositories/# Interfaces (puertos de salida)
│   ├── application/     # Casos de uso, servicios, DTOs
│   │   ├── use_cases/
│   │   ├── services/
│   │   └── dtos/
│   ├── infrastructure/  # Implementaciones concretas (ORM, auth, notificaciones, eventos)
│   │   ├── orm/
│   │   ├── repositories/
│   │   ├── database/
│   │   ├── auth/
│   │   ├── notifications/
│   │   └── events/
│   └── api/             # Rutas, dependencias, guards
│       ├── routes/
│       ├── dependencies/
│       └── guards/
├── frontend/            # Aplicación Streamlit
│   └── views/
├── docs/                # Diagramas UML
└── docker-compose.yml
```

### Principios de separación

- El **dominio** no conoce ni depende del ORM ni de FastAPI
- Los **endpoints** nunca consultan el ORM directamente; pasan por casos de uso
- Los **modelos ORM** nunca se exponen directamente por la API; se transforman en DTOs
- Las **interfaces de repositorio** viven en el dominio; sus implementaciones en infraestructura

---

## Roles y permisos

| Acción                        | OPERATOR | SUPERVISOR | ADMIN |
|-------------------------------|----------|------------|-------|
| Crear incidente               | ✅        | ✅          | ✅     |
| Ver sus propios incidentes    | ✅        | ✅          | ✅     |
| Ver todos los incidentes      | ❌        | ✅          | ✅     |
| Asignar incidente             | ❌        | ✅          | ✅     |
| Cambiar estado de incidente   | ❌        | ✅          | ✅     |
| Ver tareas asignadas          | ✅        | ✅          | ✅     |
| Ver todas las tareas          | ❌        | ✅          | ✅     |
| Ver sus notificaciones        | ✅        | ✅          | ✅     |
| Ver todas las notificaciones  | ❌        | ❌          | ✅     |

---

## Patrones de diseño implementados
### Comportamiento

| Patrón          | Dónde se aplica                          | Justificación                                                                 |
|-----------------|------------------------------------------|-------------------------------------------------------------------------------|
| **Observer**    | `domain/observers/`, `infrastructure/events/` | El Event Bus publica eventos del sistema; los observers reaccionan de forma desacoplada |
| **Command**     | `domain/commands/`                       | Encapsula el envío de notificaciones como objetos ejecutables con `execute()` |
| **State**       | `domain/states/`                         | Controla las transiciones válidas del ciclo de vida de un `Incident`          |
| **Template Method** | `domain/templates/`                 | Construye mensajes de notificación con estructura común, variando por canal   |

### Creacionales

| Patrón              | Dónde se aplica                              | Justificación                                                           |
|---------------------|----------------------------------------------|-------------------------------------------------------------------------|
| **Factory**         | `infrastructure/notifications/`              | Centraliza la creación de entidades y comandos con validaciones          |
| **Abstract Factory**| `infrastructure/notifications/`              | Agrupa la creación de providers y comandos de notificación por canal (email, in-app), garantizando consistencia entre objetos relacionados |

---

## Cómo correrlo

### Requisitos

- Docker Desktop instalado y corriendo
- Git instalado
### Pasos

```bash
git clone https://github.com/Milo18113/ds-proyecto-3.git
cd ds-proyecto-3

cp .env.example .env
# Editar .env: misma contraseña en POSTGRES_PASSWORD y en DATABASE_URL; SECRET_KEY única y larga.
docker compose up --build
```

Una vez levantado:

- **API**: `http://localhost:8000`
- **Docs de la API**: `http://localhost:8000/docs`
- **Frontend**: `http://localhost:8501`

### Detener el sistema

```bash
docker compose down
```

---
## Variables de entorno

El proyecto utiliza un archivo `.env` basado en `.env.example`.

Variables (plantilla comentada en `.env.example`):

| Variable | Uso |
|----------|-----|
| `POSTGRES_*` | Credenciales del contenedor Postgres |
| `DATABASE_URL` | Conexión SQLAlchemy (en Docker usar host `db`) |
| `SECRET_KEY` | Firma JWT (obligatoria; el backend falla si falta) |
| `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT (valores por defecto razonables en desarrollo) |
| `CORS_ORIGINS` | Orígenes permitidos para el navegador (lista separada por comas) |
| `API_BASE_URL` | URL del API para el cliente Streamlit (en Compose se fija al servicio `backend`) |

Los secretos reales solo viven en `.env` (archivo ignorado por git). No subas `.env` al repositorio.

## Cómo usarlo

1. Abrir el frontend en `http://localhost:8501`
2. Iniciar sesión con las credenciales del usuario (ver usuarios de prueba abajo)
3. Según el rol, el sistema mostrará las opciones disponibles
4. La documentación interactiva de la API está disponible en `http://localhost:8000/docs`

### Usuarios de prueba

| Email                    | Password   | Rol        |
|--------------------------|------------|------------|
| admin@opscenter.com      | admin123   | ADMIN      |
| supervisor@opscenter.com | super123   | SUPERVISOR |
| operator@opscenter.com   | oper123    | OPERATOR   |

> Los usuarios de prueba se crean automáticamente al levantar el sistema por primera vez.

---

## Endpoints principales

| Método  | Ruta                          | Descripción                        |
|---------|-------------------------------|------------------------------------|
| `POST`  | `/login`                      | Autenticación                      |
| `GET`   | `/me`                         | Usuario autenticado actual         |
| `GET`   | `/incidents`                  | Listar incidentes (según rol)      |
| `POST`  | `/incidents`                  | Crear incidente                    |
| `GET`   | `/incidents/{id}`             | Detalle de incidente               |
| `PATCH` | `/incidents/{id}/assign`      | Asignar incidente                  |
| `PATCH` | `/incidents/{id}/status`      | Cambiar estado de incidente        |
| `GET`   | `/tasks`                      | Listar tareas (según rol)          |
| `POST`  | `/tasks`                      | Crear tarea                        |
| `PATCH` | `/tasks/{id}/status`          | Cambiar estado de tarea            |
| `GET`   | `/notifications`              | Listar notificaciones (según rol)  |

---

## UML

Los diagramas se encuentran en `/docs`:

- `use_case_diagram.puml` — Actores y casos de uso del sistema
- `class_diagram.puml` — Entidades, patrones y relaciones
- `sequence_diagram.puml` — Flujo completo: creación de incidente → notificación enviada

---
