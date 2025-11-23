# Almera link shortener

## Descripción

Almera Link Shortener es una aplicación web diseñada para transformar URLs largas y complejas en enlaces cortos y fáciles de compartir. Ideal para redes sociales, correos electrónicos y cualquier situación donde la longitud del enlace sea un factor importante.

## Características

- **Acortamiento de URLs**: Convierte cualquier URL larga en un enlace conciso.
- **Redirección Rápida**: Los enlaces acortados redirigen eficientemente a la URL original.
- **Interfaz de Usuario Sencilla**: Diseño intuitivo para una experiencia de usuario fluida.
- **Historial de Enlaces (Opcional)**: Posibilidad de ver y gestionar los enlaces acortados (si se implementa autenticación).
- **Análisis Básico (Opcional)**: Métricas simples como el número de clics por enlace.

## Tecnologías Utilizadas

### Backend

- **Framework**: FastAPI 0.121.3 - Framework web moderno y de alto rendimiento para Python
- **ORM**: SQLAlchemy 2.0.44 - Manejo de base de datos con Object-Relational Mapping
- **Base de Datos**: SQLite - Base de datos ligera para desarrollo (configurable para PostgreSQL/MySQL en producción)
- **Validación**: Pydantic 2.12.4 - Validación de datos y serialización
- **Servidor ASGI**: Uvicorn 0.38.0 - Servidor de aplicaciones asíncrono de alto rendimiento
- **CORS**: Middleware configurado para permitir peticiones desde dominios autorizados (almera.es)

### Arquitectura del Backend

El backend sigue una **arquitectura en capas** limpia y modular:

#### Estructura de Capas

1. **Capa de Presentación** (`routers.py`)

   - Define los endpoints de la API REST
   - Maneja las peticiones HTTP y respuestas
   - Endpoints principales:
     - `POST /shorten` - Crear URL acortada
     - `GET /{short_code}` - Redireccionar a URL original
     - `GET /health` - Health check del servicio

2. **Capa de Lógica de Negocio** (`service.py`)

   - `URLService`: Contiene la lógica principal del acortador
   - Generación de códigos únicos con sistema de reintentos
   - Verificación de URLs duplicadas
   - Incremento de contador de visitas

3. **Capa de Acceso a Datos** (`repository.py`)

   - `URLRepository`: Patrón Repository para abstracción de datos
   - Operaciones CRUD sobre la base de datos
   - Consultas optimizadas con índices

4. **Capa de Modelos** (`models.py`)

   - Modelo `URL` con SQLAlchemy
   - Campos: id, original_url, short_code, created_at, expires_at, clicks
   - Expiración automática configurable (90 días por defecto)

5. **Capa de Validación** (`schemas.py`)
   - Schemas Pydantic para validación de entrada/salida
   - `URLCreate`: Valida URLs con formato correcto
   - `URLInfo`: Serialización de respuestas

#### Características Técnicas

- **Generación de Códigos**: Códigos aleatorios de 8 caracteres (alfanuméricos) usando `secrets` para seguridad criptográfica
- **Prevención de Duplicados**: Verifica URLs existentes antes de crear nuevos códigos
- **Sistema de Reintentos**: Hasta 5 intentos para generar códigos únicos
- **Tracking de Clicks**: Contador automático de visitas por enlace
- **Expiración de Enlaces**: Sistema de caducidad configurable
- **Inyección de Dependencias**: Uso de FastAPI Depends para gestión de sesiones de BD

## Instalación

Para configurar el proyecto localmente, sigue estos pasos:

1.  **Clona el repositorio**:

    ```bash
    git clone https://github.com/ChristianRegueiro/almera_shortener_backend.git
    cd almera_shortlink_backend
    ```

2.  **Configura el entorno virtual de Python**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configura las variables de entorno** (opcional):
    Puedes crear un archivo `.env` en la raíz del proyecto para personalizar la configuración:

    ```env
    DATABASE_URL=sqlite:///./test.db  # O PostgreSQL: postgresql://user:pass@localhost/dbname
    DEFAULT_EXPIRATION_DAYS=90
    CODE_LENGTH=8
    ```

4.  **Inicia la aplicación**:

    ```bash
    uvicorn app.main:app --reload
    ```

    La aplicación estará disponible en `http://localhost:8000`

5.  **Documentación interactiva**:
    FastAPI genera automáticamente documentación interactiva:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

## Uso

### API Endpoints

#### 1. Health Check

```bash
curl http://localhost:8000/health
```

#### 2. Acortar una URL

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.ejemplo.com/url-muy-larga"}'
```

Respuesta:

```json
{
  "id": 1,
  "original_url": "https://www.ejemplo.com/url-muy-larga",
  "short_code": "aB3dEf9H"
}
```

#### 3. Redireccionar usando código corto

```bash
curl http://localhost:8000/aB3dEf9H
```

### Estructura del Proyecto

```
almera_shortlink_backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Punto de entrada de la aplicación
│   ├── routers.py        # Definición de endpoints
│   ├── service.py        # Lógica de negocio
│   ├── repository.py     # Acceso a datos
│   ├── models.py         # Modelos SQLAlchemy
│   ├── schemas.py        # Schemas Pydantic
│   ├── db.py             # Configuración de base de datos
│   ├── settings.py       # Configuración global
│   └── utils.py          # Utilidades (generación de códigos)
├── requirements.txt      # Dependencias Python
├── test.db              # Base de datos SQLite (generada automáticamente)
└── README.md
```

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir, por favor, sigue estos pasos:

1.  Haz un "fork" de este repositorio.
2.  Crea una nueva rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3.  Realiza tus cambios y haz "commit" (`git commit -m 'feat: Añade nueva característica X'`).
4.  Haz "push" a la rama (`git push origin feature/nueva-caracteristica`).
5.  Abre un "Pull Request" describiendo tus cambios.

## Licencia

Este proyecto está bajo la licencia [Por definir, e.g., MIT License]. Consulta el archivo `LICENSE` para más detalles.

---

© 2025 Christian Regueiro
