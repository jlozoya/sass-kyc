# 🌐 Frontend — KYC Dashboard (Vue 3 + TypeScript + Vite + Tailwind)

This is the frontend for the **SaaS KYC onboarding module**, built with:

* **Vue 3 (Composition API)**
* **TypeScript**
* **Vite**
* **Vue Router**
* **Axios**
* **Tailwind CSS**

It provides a simple back-office interface for:

* Creating KYC verification requests
* Listing and searching requests
* Viewing request details
* Updating request status
* Displaying backend-generated risk scoring

---

## 📦 1. Install dependencies

Navigate to the `frontend` folder and install all packages:

```bash
npm install
```

If you see editor errors related to types (Volar / TS), restart the Vue & TS servers:

```
Ctrl + Shift + P → "Vue: Restart Vue Server"
Ctrl + Shift + P → "TypeScript: Restart TS Server"
```

---

## ⚙️ 2. Environment variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

> **Important:** All frontend environment variables must start with `VITE_` so Vite can expose them.

---

## 🚀 3. Start development server

Run the Vite dev server:

```bash
npm run dev
```

Vite will start the app at:

👉 **[http://localhost:5173](http://localhost:5173)**

The frontend will automatically communicate with the backend using
`import.meta.env.VITE_API_BASE_URL`.

---

## 🧪 4. Running frontend tests

A minimal test setup is included (Vitest or similar).

To execute frontend tests:

```bash
npm run test
```

If you used `npm create vite@latest --template vue-ts`, tests run via:

```bash
npm run test:unit
```

---

## 📁 5. Project structure

```text
frontend/
  src/
    api/              # API calls (Axios)
    components/       # Reusable UI components
    views/            # Pages (List, Form, Detail)
    router/           # Vue Router config
    assets/           # Global styles
    env.d.ts          # Vite/TS env type declarations
  public/
  index.html
  package.json
  tsconfig.json
  tailwind.config.js
```

---

## 🎨 6. Styling

Tailwind CSS is configured and enabled via:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

You can customize your Tailwind setup in:

```
tailwind.config.js
```

---

## 🔌 7. API Integration

All API calls use Axios and the base URL:

```ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
});
```

The following endpoints are consumed:

| Method | Endpoint               | Description                  |
| ------ | ---------------------- | ---------------------------- |
| GET    | `/requests`            | List requests (with filters) |
| POST   | `/requests`            | Create a new request         |
| GET    | `/requests/:id`        | Get details of a request     |
| PATCH  | `/requests/:id/status` | Update status                |

---

## ✔️ 8. Production build

Generate the optimized production bundle:

```bash
npm run build
```

Preview the build:

```bash
npm run preview
```
