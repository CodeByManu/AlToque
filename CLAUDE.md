# AlToque – Project Rules for Claude Code

## Contexto
AlToque es un sistema de micro-feedback para restaurantes que captura 
una pregunta aleatoria al momento del pago en POS. Stack: FastAPI + 
PostgreSQL + React + Kotlin (Android nativo) + Twilio (WhatsApp).

Este proyecto es un MVP para validar en un piloto de 3 semanas. 
Prioridad: que funcione end-to-end, NO sobre-ingeniería.

## Reglas de oro

1. **NUNCA** instales librerías nuevas sin avisar primero. Stack fijo:
   - Backend: FastAPI, SQLAlchemy 2.x, psycopg2-binary, pydantic v2, 
     python-dotenv, twilio, uvicorn
   - Frontend: React 18 + Vite + Tailwind + axios + react-router
   - Android: Kotlin + Jetpack Compose + Retrofit + Coroutines

2. **NUNCA** uses ORM avanzado. SQLAlchemy con `select()` plano, sin 
   relationships mágicas. Quiero ver el SQL.

3. **Errores explícitos**: cada endpoint devuelve HTTPException con 
   status code claro. Nada de `except: pass`.

4. **Logging estructurado**: usar `logging` de Python con formato 
   `[timestamp] [level] [module] mensaje`. NO `print()`.

5. **Variables de entorno**: TODO secret en `.env`. Nunca hardcodear.

6. **Commits**: si yo no te lo pido, NO hagas commits. Yo manejo git.

7. **Tests**: por ahora no escribas tests. Prioridad es velocidad de MVP.

8. **Comentarios**: solo cuando el código no se autodocumenta. 
   Comentarios en español.

9. **Antes de codear**: si algo del SPEC no está claro, PREGUNTA. 
   No improvises features no especificados.

## Cómo trabajar conmigo

- Cuando te pida una feature, primero haz un plan de 3-5 bullets 
  de qué archivos vas a tocar. Esperá mi OK.
- Después, codeá. Mostrame los cambios y esperá feedback.
- Si encontrás un bug, NO inventes solución creativa. Decime el bug.

## Archivos de referencia obligatorios

- `SPEC.md` → especificación funcional completa
- `docs/api.md` → contrato de la API REST
- `docs/db-schema.md` → esquema de PostgreSQL