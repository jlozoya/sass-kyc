# 🧩 Módulo de Onboarding KYC — Full Stack Assessment

**Vue 3 + FastAPI + MongoDB**

Este proyecto implementa un módulo ligero de onboarding KYC para uso interno en back-office.
Permite a los operadores:

* Crear solicitudes de verificación
* Subir archivos (imágenes, PDFs, Word)
* Capturar fotos usando la cámara del dispositivo
* Visualizar información del usuario y su documento
* Consultar riesgo calculado por el backend
* Actualizar el estado de una solicitud
* Eliminar solicitudes (incluye borrado automático del archivo subido)

---

# 🚀 Cómo ejecutar el proyecto

## 1. Backend — FastAPI

### Instalar dependencias

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

### Configurar MongoDB

En la consola de MongoDB:

```js
use sasskyc
db.createUser({
  user: "sasskyc",
  pwd: "CHANGE_THIS_PASSWORD!!!",
  roles: [{ role: "readWrite", db: "sasskyc" }]
})
```

Crear el archivo `backend/.env`:

```
MONGODB_URI=mongodb://sasskyc:CHANGE_THIS_PASSWORD!!!@127.0.0.1:27017/sasskyc?authSource=sasskyc
MONGODB_DB_NAME=sasskyc
```

---

### Probar la conexión a la base de datos

```bash
python tests/test_mongo.py
```

---

### Iniciar servidor FastAPI

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Swagger UI:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Carga de archivos (Uploads)

El backend expone:

```
POST /uploads/document
```

Admite:

* Imágenes: jpg, jpeg, png, webp
* PDF
* Documentos Word
* Fotografías capturadas desde la cámara

Los archivos se almacenan en:

```
/static/uploads/
```

El backend:

* Genera un nombre UUID único para el archivo almacenado
* Guarda también el **nombre original** para mostrarlo en la interfaz
* Devuelve: `url`, `filename`, `content_type`

Eliminación:
`DELETE /requests/{id}` borra el registro y **el archivo asociado**.

---

## 2. Frontend — Vue 3 + Vite

### Instalar dependencias

```bash
cd frontend
npm install
```

---

### Variables de entorno

Crear `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

---

### Iniciar en modo desarrollo

```bash
npm run dev
```

Aplicación disponible en:
👉 [http://localhost:5173](http://localhost:5173)

---

# 🛠️ Tecnologías utilizadas

## Backend

* **FastAPI**
* **Motor (async MongoDB)**
* **Pydantic v2**
* **Uvicorn**
* **Sistema de archivos estáticos**
* **pytest**

## Frontend

* **Vue 3 (Composition API)**
* **TypeScript**
* **Vite**
* **Tailwind CSS**
* **Vue Router**
* **Utilidad fetch personalizada para APIs**
* **Captura de cámara con MediaStream API**

## Base de Datos

* **MongoDB**

---

# 🧠 Decisiones técnicas clave

### ✔ MongoDB + Motor

* Esquema flexible
* Gran velocidad de desarrollo
* Integración natural con FastAPI async

### ✔ Arquitectura del backend organizada

```
api/        → endpoints (requests, uploads)
core/       → configuración y conexión con BD
schemas/    → modelos Pydantic v2
services/   → lógica de negocio (motor de riesgo)
static/     → almacenamiento de archivos subidos
```

### ✔ Motor de riesgo desacoplado

Reglas simples pero claras:

* Dominios de email sospechosos
* Países restringidos
* Longitud válida del número de documento

Genera un nivel de riesgo: **low**, **medium**, **high**

### ✔ Carga de archivos y cámara

El frontend permite:

* Subir archivos manualmente
* Tomar fotos desde la cámara
* Previsualizar o descargar documentos
* Ocultar/mostrar controles dinámicamente
* Guardar el nombre original del archivo

### ✔ Eliminación de solicitudes

`DELETE /requests/{id}`:

* Elimina la solicitud
* Elimina el archivo del servidor
* Devuelve `204 No Content`
* El frontend redirige automáticamente al listado

---

# ⚠️ Limitaciones actuales

* No incluye autenticación de operadores
* Sin paginación en la tabla de solicitudes
* Motor de riesgo básico (reglas estáticas)
* El almacenamiento de archivos es local (no S3 u otro servicio cloud)

---

# 🧪 Pruebas automatizadas

## Backend

```bash
cd backend
pytest
```

Incluye:

* Pruebas del motor de riesgo
* Validación del documento de solicitud

---

## Frontend

```bash
cd frontend
npm run test
```

Incluye:

* Pruebas de componentes
* Utilidades independientes
