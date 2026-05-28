# AlToque

Sistema de micro-feedback para restaurantes. Al momento del pago, la tablet del POS muestra una pregunta aleatoria al cliente (ej. "¿Cómo estuvo la comida?"). El cliente responde con una carita (1–5) o la omite. Si el rating es ≤ 2, se envía una alerta automática por WhatsApp al gerente vía Twilio.

El sistema consta de tres partes:

- **Backend** – API REST + WebSocket (FastAPI + PostgreSQL)
- **Dashboard** – Panel de métricas en tiempo real (React + Vite + Tailwind)
- **App Android** – Plugin para la tablet del POS (Kotlin + Jetpack Compose)

---

## Requisitos previos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Android Studio (para la app)
- Cuenta Twilio con WhatsApp habilitado

---

## 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en `backend/`:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/altoque
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
MANAGER_WHATSAPP_TO=whatsapp:+569XXXXXXXX
LOG_LEVEL=INFO
```

```bash
alembic upgrade head          # crea las tablas
uvicorn app.main:app --reload # inicia en http://localhost:8000
```

Seed inicial (crea restaurante, mesas, garzones y preguntas de prueba):

```bash
curl -X POST http://localhost:8000/api/v1/admin/seed
```

---

## 2. Dashboard

```bash
cd dashboard
npm install
```

Crea un archivo `.env` en `dashboard/`:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_RESTAURANT_ID=<uuid devuelto por el seed>
```

```bash
npm run dev   # inicia en http://localhost:5173
```

---

## 3. App Android

Abre la carpeta `android/` en Android Studio.

Agrega en `local.properties`:

```properties
API_BASE_URL_DEBUG=http://10.0.2.2:8000
API_BASE_URL_RELEASE=https://altoque-api.up.railway.app
RESTAURANT_ID=<uuid devuelto por el seed del backend>
```

> `10.0.2.2` es el equivalente a `localhost` del host desde el emulador Android.

> `local.properties` está en `.gitignore` — nunca se commitea.

Ejecuta el build **debug** apuntando al backend local, o **release** para producción.

---

## Flujo completo

1. El garzón selecciona mesa y su nombre en la tablet.
2. Al cerrar la mesa, aparece una pregunta aleatoria.
3. El cliente toca una carita (1–5) o "Omitir".
4. El backend registra la respuesta. Si rating ≤ 2, envía alerta WhatsApp.
5. El dashboard muestra métricas e historial en tiempo real vía WebSocket.
