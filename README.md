# 🚀 Portal AYMA Advisors - Backend API

API REST del Portal de Clientes para AYMA Advisors.

## 📋 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos para desarrollo local
- **PostgreSQL** - Base de datos para producción
- **JWT** - Autenticación con tokens
- **Pydantic** - Validación de datos

## 🏗️ Estructura del Proyecto

```
backend/
├── app/
│   ├── core/           # Configuración, DB, seguridad
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── api/
│   │   └── v1/         # Endpoints API
│   ├── services/       # Lógica de negocio
│   ├── utils/          # Utilidades
│   └── main.py         # Aplicación principal
├── requirements.txt    # Dependencias
├── .env.example        # Ejemplo de variables de entorno
└── README.md          # Este archivo
```

## 🚀 Instalación y Uso

### 1. Instalar Dependencias

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar ejemplo de .env
cp .env.example .env

# Editar .env con tus valores
# Para desarrollo local, los valores por defecto están bien
```

### 3. Iniciar el Servidor

```bash
# Desde el directorio backend/
uvicorn app.main:app --reload

# O ejecutar directamente:
python -m app.main
```

El servidor estará disponible en: http://localhost:8000

## 📚 Documentación de la API

Una vez iniciado el servidor, la documentación interactiva está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Login de usuario
- `POST /api/v1/auth/refresh` - Refrescar token
- `GET /api/v1/auth/me` - Info del usuario actual
- `POST /api/v1/auth/change-password` - Cambiar contraseña

### Dashboard
- `GET /api/v1/dashboard/` - Resumen del dashboard
- `GET /api/v1/dashboard/scoring` - Scoring del cliente
- `GET /api/v1/dashboard/actividades` - Actividades recientes

### Pólizas
- `GET /api/v1/polizas/` - Listar pólizas del cliente
- `GET /api/v1/polizas/{id}` - Detalle de póliza
- `GET /api/v1/polizas/{id}/pdf` - Descargar PDF de póliza

### Vehículos
- `GET /api/v1/vehiculos/` - Listar vehículos del cliente
- `GET /api/v1/vehiculos/{id}` - Detalle de vehículo
- `GET /api/v1/vehiculos/{id}/polizas` - Pólizas de un vehículo

## 🗄️ Base de Datos

### Desarrollo Local (SQLite)
Por defecto usa SQLite, no necesitas instalar nada.
El archivo de base de datos se crea automáticamente: `ayma_portal.db`

### Producción (PostgreSQL)
En Railway, la base de datos PostgreSQL se configura automáticamente.
Solo necesitas actualizar la variable `DATABASE_URL` en las variables de entorno.

## 🔐 Sistema de Scoring

El sistema de scoring automático registra puntos por cada acción:

| Acción | Puntos |
|--------|--------|
| Login | 1 |
| Ver póliza | 2 |
| Descargar PDF | 3 |
| Solicitar cotización | 13 |
| Llamado nuevo | 5.9 |
| Cotizado | 13 |
| Propuesta entregada | 25 |
| Cliente cerrado | 50 |
| Cliente perdido | -50 |

**Objetivos:**
- Diario: 130 puntos
- Semanal: 840 puntos

## 🧪 Testing

Para probar la API puedes usar:

1. **Swagger UI** (http://localhost:8000/docs)
2. **Postman** o **Insomnia**
3. **cURL** desde la terminal

### Ejemplo de Login con cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente.prueba@ayma.com.ar",
    "password": "password123"
  }'
```

## 📦 Deploy en Railway

1. **Conectar repositorio en Railway**
2. **Agregar PostgreSQL addon**
3. **Configurar variables de entorno:**
   - `DATABASE_URL` (se configura automáticamente con PostgreSQL)
   - `SECRET_KEY` (generar una clave segura)
   - `FRONTEND_URL` (URL del frontend en Vercel)
   - `ENVIRONMENT=production`

4. **Railway detecta automáticamente FastAPI y lo deploya**

## 🔧 Comandos Útiles

```bash
# Ver logs en desarrollo
uvicorn app.main:app --reload --log-level debug

# Crear migración de base de datos (con Alembic, para futuro)
# alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
# alembic upgrade head

# Formatear código (si usas black)
# black app/

# Linting (si usas flake8)
# flake8 app/
```

## 📝 Notas Importantes

1. **SQLite para desarrollo** - Perfecto para desarrollo local, no necesitas instalar PostgreSQL
2. **PostgreSQL para producción** - Railway maneja esto automáticamente
3. **JWT Tokens** - Los tokens expiran en 30 minutos, usar refresh token para renovar
4. **CORS** - Ya configurado para localhost y Vercel
5. **Scoring automático** - Se registra en cada acción del cliente

## 🆘 Troubleshooting

### Error: "No module named 'app'"
```bash
# Asegurarte de estar en el directorio backend/ al ejecutar
cd backend
uvicorn app.main:app --reload
```

### Error: "Table already exists"
```bash
# Eliminar base de datos y dejar que se recree
rm ayma_portal.db
# Reiniciar servidor
```

### Error: "Port already in use"
```bash
# Usar otro puerto
uvicorn app.main:app --reload --port 8001
```

## 🎯 Próximos Pasos

- [ ] Implementar generación real de PDFs
- [ ] Agregar envío de emails
- [ ] Integrar WhatsApp
- [ ] Agregar más endpoints administrativos
- [ ] Implementar cache con Redis
- [ ] Tests unitarios

## 📧 Contacto

Sebastián - AYMA Advisors
www.aymaadvisors.com.ar
