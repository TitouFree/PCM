from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import re
import ipaddress
import logging
from pathlib import Path
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlparse
import httpx

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)

EMAIL_BASE_URL = "https://integrations.emergentagent.com"
EMAIL_KEY = os.environ.get("EMERGENT_EMAIL_KEY", "")
EMAIL_FROM_NAME = os.environ.get("EMAIL_FROM_NAME", "Paris Carrelages et Matériaux")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "")

_SHORTENERS = ("bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "goo.gl", "rebrand.ly")
_CRED_ASK = ("reply with your password", "reply with the code", "send your password", "cvv",
             "send us your password", "enter your password below", "confirm your card number",
             "your full card number", "seed phrase", "recovery phrase", "verify your card",
             "social security number", "confirm your bank details")
_HOSTISH = re.compile(r"\b(?:https?://)?((?:[a-z0-9-]+\.)+[a-z]{2,})", re.I)


def _host_ok(host: str) -> bool:
    if not host or "xn--" in host:
        return False
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    return not any(host == s or host.endswith("." + s) for s in _SHORTENERS)


def _same_site(shown: str, real: str) -> bool:
    return shown == real or real.endswith("." + shown) or shown.endswith("." + real)


class _EmailScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.urls, self.anchors = set(), [], []
        self._href, self._text = None, []

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag.lower())
        self.urls += [v for k, v in attrs if k.lower() in ("href", "src") and v]
        if tag.lower() == "a":
            self._href = dict((k.lower(), v) for k, v in attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.anchors.append((self._href, "".join(self._text)))
            self._href, self._text = None, []


def _assert_safe_email(subject: str, html: str) -> None:
    scan = _EmailScan()
    scan.feed(html)
    if scan.tags & {"form", "input", "textarea", "select"}:
        raise ValueError("No forms or input fields in email (G2)")
    body = f"{subject}\n{html}".lower()
    for p in _CRED_ASK:
        if p in body:
            raise ValueError(f"Email asks the recipient for credentials: {p!r} (G2)")
    for url in scan.urls:
        low = url.strip().lower()
        if low.startswith(("mailto:", "tel:", "cid:", "#")):
            continue
        if not low.startswith("https://"):
            raise ValueError(f"Email links/assets must be absolute https: {url!r} (G3)")
        host = urlparse(low).hostname or ""
        if not _host_ok(host) or urlparse(low).username is not None:
            raise ValueError(f"Shortened, numeric-host or credential-bearing URL: {url!r} (G3)")
    for href, text in scan.anchors:
        real = urlparse(href.strip().lower()).hostname or ""
        if not real:
            continue
        for m in _HOSTISH.finditer(text):
            if not _same_site(m.group(1).lower(), real):
                raise ValueError(f"Anchor text {m.group(1)!r} != real link host {real!r} (G3)")


async def send_email(*, to: str, subject: str, html: str, reply_to: Optional[str] = None) -> Optional[str]:
    _assert_safe_email(subject, html)
    payload = {"to": [to], "subject": subject, "html": html, "from_name": EMAIL_FROM_NAME}
    if reply_to:
        payload["contact_email"] = reply_to
    try:
        async with httpx.AsyncClient(timeout=30) as client_http:
            resp = await client_http.post(
                f"{EMAIL_BASE_URL}/api/v1/email/send",
                headers={"X-Email-Key": EMAIL_KEY},
                json=payload,
            )
        resp.raise_for_status()
        return resp.json().get("id")
    except httpx.HTTPStatusError as e:
        logger.error(f"Email send failed: {e.response.status_code} {e.response.text}")
        raise HTTPException(status_code=502, detail="Failed to send email")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email send error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send email")


class DevisRequest(BaseModel):
    nom: str
    email: EmailStr
    telephone: str
    profil: str = "Particulier"
    familles: List[str] = []
    message: str
    adresse_chantier: Optional[str] = None
    delai: Optional[str] = None


@api_router.get("/")
async def root():
    return {"message": "Paris Carrelages et Matériaux — API"}


@api_router.get("/health")
async def health():
    return {"status": "ok"}


@api_router.post("/devis")
async def create_devis(input: DevisRequest):
    if len(input.nom) > 120 or len(input.message) > 4000:
        raise HTTPException(status_code=422, detail="Champs trop longs")
    doc = input.model_dump()
    doc["email"] = str(input.email)
    doc["request_id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    await db.devis_requests.insert_one(doc)

    def row(label, value):
        return (f'<tr><td style="padding:6px 12px;font-weight:bold;color:#0D3A5C;'
                f'vertical-align:top;white-space:nowrap">{escape(label)}</td>'
                f'<td style="padding:6px 12px;color:#1F2226">{value}</td></tr>')

    familles = ", ".join(escape(f) for f in input.familles) if input.familles else "Non précisé"
    rows = "".join([
        row("Nom", escape(input.nom)),
        row("Profil", escape(input.profil)),
        row("Téléphone", escape(input.telephone)),
        row("E-mail", escape(str(input.email))),
        row("Familles concernées", familles),
        row("Adresse du chantier", escape(input.adresse_chantier or "Non précisée")),
        row("Délai souhaité", escape(input.delai or "Non précisé")),
        row("Message", escape(input.message).replace("\n", "<br>")),
    ])
    html = (
        '<table role="presentation" width="100%" style="background:#F6F4ED;padding:24px">'
        '<tr><td style="font-family:Arial,sans-serif">'
        '<h2 style="color:#0D3A5C;margin:0 0 12px">Nouvelle demande de devis</h2>'
        f'<table role="presentation" style="background:#ffffff;border:1px solid #DDD8D0">{rows}</table>'
        f'<p style="font-size:12px;color:#8E949D;margin-top:16px">Envoyé depuis le site '
        f'{escape(EMAIL_FROM_NAME)} — pariscarrelages.fr. Répondez directement à ce message '
        f'pour écrire au demandeur.</p>'
        '</td></tr></table>'
    )
    email_id = None
    if OWNER_EMAIL and EMAIL_KEY:
        email_id = await send_email(
            to=OWNER_EMAIL,
            subject=f"Demande de devis — {input.nom}",
            html=html,
            reply_to=str(input.email),
        )
    return {"status": "success", "request_id": doc["request_id"], "email_id": email_id}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
