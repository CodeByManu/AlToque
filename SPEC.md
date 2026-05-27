# AlToque – Especificación técnica MVP

## 1. Componentes

### 1.1 Backend (FastAPI)
URL local: `http://localhost:8000`
URL prod: `https://altoque-api.up.railway.app` (Railway)

### 1.2 Dashboard (React + Vite)
URL local: `http://localhost:5173`
URL prod: `https://altoque-dashboard.up.railway.app`

### 1.3 App Android (Kotlin)
Apunta a la URL de backend según build flavor (debug = local, 
release = prod).

## 2. Esquema de base de datos (PostgreSQL)

### Tabla `restaurants`
- id: uuid PK
- name: varchar(100)
- created_at: timestamp

### Tabla `waiters` (garzones)
- id: uuid PK
- restaurant_id: uuid FK
- name: varchar(100)
- active: boolean

### Tabla `tables` (mesas)
- id: uuid PK
- restaurant_id: uuid FK
- number: int
- active: boolean

### Tabla `questions`
- id: uuid PK
- restaurant_id: uuid FK
- text: varchar(200)
- category: varchar(50) -- 'comida', 'servicio', 'espera', 'ambiente', 'general'
- active: boolean

### Tabla `responses`
- id: uuid PK
- restaurant_id: uuid FK
- table_id: uuid FK
- waiter_id: uuid FK
- question_id: uuid FK NULL -- NULL si fue 'omitir'
- rating: int NULL -- 1 a 5, NULL si fue omitir
- action: varchar(10) -- 'answered' | 'skipped'
- shown_at: timestamp -- cuando se mostró la pregunta
- responded_at: timestamp -- cuando respondió
- interaction_ms: int -- responded_at - shown_at en milisegundos
- created_at: timestamp

### Tabla `alerts`
- id: uuid PK
- response_id: uuid FK
- restaurant_id: uuid FK
- whatsapp_status: varchar(20) -- 'pending' | 'sent' | 'failed'
- whatsapp_message_sid: varchar(100) NULL
- sent_at: timestamp NULL
- created_at: timestamp

## 3. Endpoints REST

### Para el plugin Android (consumidos por la tablet)

**GET `/api/v1/sessions/start`**
Query params: `restaurant_id`, `table_id`, `waiter_id`
Response 200:
```json
{
  "session_id": "uuid",
  "question": {
    "id": "uuid",
    "text": "¿Cómo estuvo la comida?",
    "category": "comida"
  },
  "shown_at": "2026-06-10T14:23:11Z"
}
```

**POST `/api/v1/responses`**
Body:
```json
{
  "session_id": "uuid",
  "question_id": "uuid",
  "rating": 4,
  "action": "answered",
  "shown_at": "2026-06-10T14:23:11Z",
  "responded_at": "2026-06-10T14:23:14Z"
}
```
Si `rating <= 2`: dispara alerta WhatsApp asíncronamente.
Response 201 con el response creado.

### Para el dashboard (consumidos por React)

**GET `/api/v1/dashboard/metrics?restaurant_id=...`**
Response 200:
```json
{
  "total_responses": 87,
  "total_skipped": 12,
  "response_rate": 0.879,
  "avg_rating": 4.2,
  "avg_interaction_ms": 2340,
  "rating_distribution": {"1": 2, "2": 3, "3": 8, "4": 34, "5": 40},
  "by_category": {
    "comida": {"count": 23, "avg": 4.3},
    "servicio": {"count": 19, "avg": 4.1}
  },
  "active_alerts": 1
}
```

**GET `/api/v1/dashboard/responses/recent?restaurant_id=...&limit=20`**
Lista de últimas respuestas con join a question, table, waiter.

**GET `/api/v1/dashboard/alerts?restaurant_id=...`**
Lista de alertas activas (últimas 24h).

### WebSocket

**WS `/ws/dashboard/{restaurant_id}`**
Emite eventos en tiempo real:
```json
{"type": "new_response", "data": {...}}
{"type": "new_alert", "data": {...}}
```

### Admin (para seed inicial, NO expuesto al público)

**POST `/api/v1/admin/seed`**
Crea restaurante de prueba con 3 mesas, 3 garzones, 5 preguntas.
Solo si la BD está vacía.

## 4. Flujo Android

1. Pantalla inicial: selector de mesa + garzón (mock del flujo del POS real)
2. Botón "Cerrar mesa" → llama `GET /sessions/start` → muestra pregunta
3. Pantalla pregunta: texto grande, 5 botones con caritas (1-5) + 
   botón "Omitir"
4. Toque → registra `responded_at` → llama `POST /responses`
5. Pantalla "Procesando pago..." (3 segundos hardcoded)
6. Pantalla "Gracias" con QR placeholder (D7 implementamos QR real)
7. Auto-volver a pantalla inicial después de 5s

## 5. Variables de entorno

### Backend `.env`
```env
DATABASE_URL=postgresql://user:pass@host:5432/altoque
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
MANAGER_WHATSAPP_TO=whatsapp:+569XXXXXXXX
LOG_LEVEL=INFO
```

### Dashboard `.env`
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_RESTAURANT_ID=<uuid del seed>
```

### Android `local.properties`
```properties
API_BASE_URL_DEBUG=http://10.0.2.2:8000
API_BASE_URL_RELEASE=https://altoque-api.up.railway.app
```

(`10.0.2.2` es localhost del host desde el emulador Android)

## 6. Reglas de negocio

- Selección de pregunta: al llamar `/sessions/start`, el backend 
  elige UNA pregunta del pool activo del restaurante con probabilidad 
  uniforme. Si una pregunta tuvo <X respuestas recientes y otras >Y, 
  preferir la menos respondida (round-robin ponderado). Para MVP: 
  random uniforme está OK.
- Alerta: si `rating <= 2`, encolar envío de WhatsApp. El mensaje es:
```
🚨 AlToque – Alerta {restaurant_name}
Mesa {table_number} · Garzón {waiter_name}
Pregunta: "{question_text}"
Rating: {rating}/5
Hora: {responded_at}
```
- Si Twilio falla, registrar `whatsapp_status='failed'`, no romper el flujo.

## 7. Out of scope para MVP

- Autenticación (todo abierto, asumimos red privada)
- Multi-tenancy real (un solo restaurante en el seed)
- Generación de QR real (mock visual hasta D7)
- Encuesta extendida web (D7)
- Tests automatizados
- CI/CD (deploy manual a Railway)