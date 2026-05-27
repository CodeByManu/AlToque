import os
from dotenv import load_dotenv

load_dotenv()


def _required(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Variable de entorno requerida no definida: {key}")
    return val


DATABASE_URL: str = _required("DATABASE_URL")

TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM: str = os.getenv("TWILIO_WHATSAPP_FROM", "")
MANAGER_WHATSAPP_TO: str = os.getenv("MANAGER_WHATSAPP_TO", "")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

ALLOWED_ORIGINS: list[str] = [
    o.strip()
    for o in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,https://altoque-dashboard.up.railway.app",
    ).split(",")
    if o.strip()
]


def twilio_configured() -> bool:
    return all(
        [
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN,
            TWILIO_WHATSAPP_FROM,
            MANAGER_WHATSAPP_TO,
        ]
    )
