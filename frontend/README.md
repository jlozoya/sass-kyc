# 🌐 Frontend — Dashboard KYC (Vue 3 + TypeScript + Vite + Tailwind)

Este es el frontend para el módulo de **onboarding KYC**, construido con:

* **Vue 3 (Composition API)**
* **TypeScript**
* **Vite**
* **Vue Router**
* **Tailwind CSS**
* **Fetch API personalizada**
* **MediaStream API** (para captura de cámara)

Proporciona una interfaz de back-office donde los operadores pueden:

* Crear nuevas solicitudes KYC
* Subir documentos o tomar fotos desde la cámara
* Mostrar el nombre original del archivo subido
* Listar y filtrar solicitudes
* Ver información detallada de una solicitud
* Descargar documentos subidos
* Actualizar el estado de una solicitud
* Eliminar solicitudes (incluye borrado del archivo en backend)
* Ver la clasificación de riesgo generada por el backend

---

## 📦 1. Instalación de dependencias

Dentro del directorio `frontend`, instala los paquetes:

```bash
npm install
```

Si el editor muestra advertencias de Typescript o Vue (Volar), reinicia los servidores:

```
Ctrl + Shift + P → "Vue: Restart Vue Server"
Ctrl + Shift + P → "TypeScript: Restart TS Server"
```

---

## ⚙️ 2. Variables de entorno

Crear un archivo `.env` en `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

> ⚠️ **Importante:** todas las variables deben empezar por `VITE_` para que Vite las exponga al código del cliente.

---

## 🚀 3. Iniciar servidor de desarrollo

Ejecuta el servidor Vite:

```bash
npm run dev
```

La app quedará disponible en:

👉 **[http://localhost:5173](http://localhost:5173)**

El frontend se conectará al backend usando:

```ts
import.meta.env.VITE_API_BASE_URL
```

---

## 📥 4. Subida de Archivos y Cámara

El frontend soporta:

* Subida de imágenes (JPG/PNG/WEBP)
* Subida de PDFs y Word
* Captura de fotos desde la cámara
* Ocultar/mostrar controles según se suba o elimine un archivo
* Previsualización de imágenes o botón de descarga para otros archivos
* Limpieza del estado cuando se elimina un archivo
* Envío del **nombre original del archivo** al backend

Los archivos se suben al endpoint:

```
POST /uploads/document
```

con respuesta:

```json
{
  "url": "/static/uploads/<uuid>.jpg",
  "filename": "nombre_original.jpg",
  "content_type": "image/jpeg"
}
```

---

## 🧪 5. Ejecutar pruebas frontend

```bash
npm run test
```

Si se usa una plantilla con Vitest:

```bash
npm run test:unit
```

---

## 📁 6. Estructura del proyecto

```
frontend/
  src/
    api/              # Clientes API (fetch)
    components/       # Componentes reutilizables
    views/            # Páginas (Listado, Formulario, Detalle)
    router/           # Configuración de Vue Router
    types/            # Tipos TS centralizados
    assets/           # Estilos/globales
    env.d.ts          # Tipado de variables Vite
  public/
  index.html
  package.json
  tsconfig.json
  tailwind.config.js
```

---

## 🔌 7. Integración con la API

El cliente HTTP usa `fetch` con un wrapper centralizado.

Ejemplo:

```ts
const API_BASE = import.meta.env.VITE_API_BASE_URL
```

Endpoints consumidos:

| Método | Endpoint               | Descripción                           |
| ------ | ---------------------- | ------------------------------------- |
| GET    | `/requests`            | Listado con filtros                   |
| POST   | `/requests`            | Crear solicitud                       |
| GET    | `/requests/:id`        | Detalles de la solicitud              |
| PATCH  | `/requests/:id/status` | Actualizar estado                     |
| DELETE | `/requests/:id`        | Eliminar solicitud + archivo asociado |
| POST   | `/uploads/document`    | Subir archivo o foto capturada        |

---

## 🎨 8. Estilos

Tailwind está habilitado mediante:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

La configuración se encuentra en:

```
tailwind.config.js
```

---

## ✔️ 9. Build de producción

Crear build optimizado:

```bash
npm run build
```

Previsualizar:

```bash
npm run preview
```
