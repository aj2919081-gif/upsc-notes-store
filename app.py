"""UPSC Notes Store"""

import os
import sqlite3
import secrets
import uuid
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, session,
    send_from_directory, abort, flash, jsonify, Response
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

try:
    import razorpay
    _razorpay_available = True
except ImportError:
    razorpay = None
    _razorpay_available = False

from _embedded_templates import TEMPLATES as EMBEDDED_TEMPLATES
from _qr_embed import UPI_QR_BASE64

# ============================================================
# CONFIGURATION - yahan aap apni settings badal sakte hain
# ============================================================
# Robust path finding: files kabhi bhi kisi bhi nesting mein ho sakti hain.
# Ye helper RECURSIVELY templates/ folder dhoondta hai (chahe wo kahi bhi ho).
def _deep_search_for_template_dir(start):
    """Start ke neeche recursively 'templates' folder dhoondo jisme index.html hai."""
    import sys
    found = []
    stack = [start]
    visited = set()
    max_scan = 20000
    count = 0
    while stack and count < max_scan:
        cur = stack.pop()
        count += 1
        if cur in visited:
            continue
        visited.add(cur)
        try:
            entries = os.listdir(cur)
        except OSError:
            continue
        for name in entries:
            full = os.path.join(cur, name)
            try:
                if os.path.isdir(full):
                    if name == "templates" and os.path.isfile(os.path.join(full, "index.html")):
                        found.append(full)
                    else:
                        # skip venv/node_modules/.venv to avoid huge scans
                        if name in (".venv", "venv", "node_modules", ".git", "__pycache__", "site-packages"):
                            continue
                        stack.append(full)
            except OSError:
                continue
    if found:
        # sabse chhota path (root ke sabse paas) choose karo
        found.sort(key=lambda p: len(p))
        return found[0]
    return None


def _find_project_root():
    here = os.path.dirname(os.path.abspath(__file__))
    t = _deep_search_for_template_dir(here)
    if t:
        return os.path.dirname(t)  # templates ka parent = project root
    return here


PROJECT_ROOT = _find_project_root()
BASE_DIR = PROJECT_ROOT
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PDF_FOLDER = os.path.join(UPLOAD_FOLDER, "pdfs")
HTML_FOLDER = os.path.join(UPLOAD_FOLDER, "html")
UPI_FOLDER = os.path.join(UPLOAD_FOLDER, "upi")
DB_PATH = os.path.join(BASE_DIR, "upsc.db")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Agar templates kisi aur jagah mila ho, wahan bhi db/static dhoondo
if not os.path.isdir(TEMPLATES_DIR):
    t = _deep_search_for_template_dir(os.path.dirname(os.path.abspath(__file__)))
    if t:
        TEMPLATES_DIR = t
        candidate_static = os.path.join(os.path.dirname(t), "static")
        if os.path.isdir(candidate_static):
            STATIC_DIR = candidate_static
        candidate_uploads = os.path.join(os.path.dirname(t), "uploads")
        if os.path.isdir(candidate_uploads):
            UPLOAD_FOLDER = candidate_uploads
        candidate_db = os.path.join(os.path.dirname(t), "upsc.db")
        if os.path.isfile(candidate_db):
            DB_PATH = candidate_db

print(f"[startup] PROJECT_ROOT = {PROJECT_ROOT}")
print(f"[startup] TEMPLATES_DIR = {TEMPLATES_DIR} (exists={os.path.isdir(TEMPLATES_DIR)})")
print(f"[startup] DB_PATH = {DB_PATH} (exists={os.path.isfile(DB_PATH)})")
print(f"[startup] UPLOAD_FOLDER = {UPLOAD_FOLDER} (exists={os.path.isdir(UPLOAD_FOLDER)})")

# ---- Aapki settings ----
# SECURITY: Secrets (password/token/session/razorpay) sirf ENVIRONMENT VARIABLES
# se aate hain — code ya repo mein hardcode NAHI karna (pehle wo public repo mein
# committed the, isliye sab rotate kar diya gaya hai — SETUP.md dekho).
SITE_NAME = "UPSC Notes Store"
SITE_TAGLINE = "Premium UPSC Notes — Ek Jagah, Sab Subjects"
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "")
# Admin panel ka SECRET URL path — sirf aapko pata hona chahiye.
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
ADMIN_PREFIX = "/" + ADMIN_TOKEN

# FREE subjects — in subjects ke notes bina login/payment ke sabko free milenge.
# (jaise PYQs, Current Affairs). Yahan aur subjects add kar sakte hain.
FREE_SUBJECTS = {"pyqs", "current-affairs"}

# UPI / contact details (buyer ke liye public business info — buy page par dikhate hain)
UPI_ID = os.environ.get("UPI_ID", "")
UPI_QR_FILENAME = "qr.png"
SELLER_PHONE = os.environ.get("SELLER_PHONE", "")
SELLER_WHATSAPP = os.environ.get("SELLER_WHATSAPP", "")
SELLER_EMAIL = os.environ.get("SELLER_EMAIL", "")

# Razorpay (live keys Razorpay dashboard se leke env vars mein set karein)
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

ALLOWED_EXTENSIONS = {"pdf", "html", "htm"}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max file

# ---- Startup security check: secrets missing ho toh app start hi NAHI hoti ----
_missing = [k for k, v in (
    ("ADMIN_PASSWORD", ADMIN_PASSWORD),
    ("ADMIN_TOKEN", ADMIN_TOKEN),
    ("SESSION_SECRET", SESSION_SECRET),
) if not v]
if _missing:
    raise SystemExit(
        "FATAL: env vars missing: " + ", ".join(_missing) + ". "
        "Render dashboard (ya local par `export VAR=...`) mein set karein. "
        "Secrets code/repo mein hardcode nahi karna — SETUP.md dekho."
    )
if len(ADMIN_PASSWORD) < 8:
    print("WARNING: ADMIN_PASSWORD 8 characters se chhota hai — strong password set karein.")

# ---- Common UPSC subjects (pehle se add kiye hue) ----
DEFAULT_SUBJECTS = [
    {"slug": "geography", "name": "Geography", "hindi": "भूगोल"},
    {"slug": "polity", "name": "Polity", "hindi": "राजव्यवस्था"},
    {"slug": "economics", "name": "Economics", "hindi": "अर्थव्यवस्था"},
    {"slug": "history", "name": "History", "hindi": "इतिहास"},
    {"slug": "science-tech", "name": "Science & Tech", "hindi": "विज्ञान और प्रौद्योगिकी"},
    {"slug": "environment", "name": "Environment & Ecology", "hindi": "पर्यावरण और पारिस्थितिकी"},
    {"slug": "art-culture", "name": "Art & Culture", "hindi": "कला और संस्कृति"},
    {"slug": "current-affairs", "name": "Current Affairs", "hindi": "समसामयिक"},
    {"slug": "ethics", "name": "Ethics", "hindi": "नैतिकता"},
    {"slug": "ir", "name": "International Relations", "hindi": "अंतर्राष्ट्रीय संबंध"},
    {"slug": "internal-security", "name": "Internal Security", "hindi": "आंतरिक सुरक्षा"},
    {"slug": "indian-society", "name": "Indian Society", "hindi": "भारतीय समाज"},
    {"slug": "csat", "name": "CSAT", "hindi": "सीसैट"},
    {"slug": "prelims", "name": "Prelims", "hindi": "प्रारंभिक"},
    {"slug": "mains", "name": "Mains Answer Writing", "hindi": "मुख्य परीक्षा"},
    {"slug": "pyqs", "name": "PYQs", "hindi": "पिछले वर्ष प्रश्न"},
    {"slug": "other", "name": "Other", "hindi": "अन्य"},
]

# ============================================================
# APP SETUP
# ============================================================
# Custom Jinja loader: sab templates embedded python module se milti hain,
# isliye alag templates/ folder ki zaroorat nahi (deploy 100% bulletproof).
from jinja2 import BaseLoader, TemplateNotFound as JinjaTemplateNotFound

class EmbeddedTemplateLoader(BaseLoader):
    def get_source(self, environment, template):
        if template in EMBEDDED_TEMPLATES:
            return EMBEDDED_TEMPLATES[template], "<embedded>", lambda: False
        raise JinjaTemplateNotFound(template)

app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)
app.jinja_loader = EmbeddedTemplateLoader()
app.secret_key = SESSION_SECRET
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
# Session cookies: SameSite=Lax (CSRF mitigation) + Secure (sirf HTTPS par cookie).
# Local HTTP testing ke liye: SESSION_COOKIE_INSECURE=1
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_INSECURE", "0") != "1"


# ---- Security headers (sab responses par) ----
_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    # Razorpay checkout CDN + templates ke inline scripts/styles ke liye allow.
    # (HTML notes ka stored-XSS iska FIX nahi hai — uske liye sandbox chahiye.)
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://checkout.razorpay.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "frame-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
    ),
}


# ---- CSRF protection ----
# Har session ko ek random token milta hai; saare POST forms mein hidden
# input `csrf_token` hona chahiye (templates mein {{ csrf_token }} hai).
# Iske bina koi bhi POST 403 deta hai (SameSite cookie ke saath double cover).
@app.context_processor
def inject_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["csrf_token"]}


@app.before_request
def csrf_protect():
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        tok = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token") or ""
        if not tok or not secrets.compare_digest(tok, session.get("csrf_token", "")):
            abort(403)


@app.errorhandler(403)
def forbidden(e):
    return Response(
        "<!DOCTYPE html><html lang='hi'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>403 — Access Denied</title></head>"
        "<body style='font-family:sans-serif;max-width:520px;margin:60px auto;padding:0 20px;text-align:center;'>"
        "<div style='font-size:64px;'>🔒</div><h2>Request reject ho gayi (403)</h2>"
        "<p>Iska matlab page bina refresh ke form submit hua, ya session expire ho gaya. "
        "Page <b>refresh</b> karke dobara try karein.</p>"
        "<a href='/' style='color:#2d0d66;font-weight:600;'>← Home chalein</a>"
        "</body></html>",
        status=403,
        mimetype="text/html",
    )


# ---- Open-redirect protection (login/signup ka `next` param) ----
def safe_next(url, fallback):
    """Sirf same-site relative paths allow karo; external URL toh fallback."""
    if not url:
        return fallback
    from urllib.parse import urlparse
    p = urlparse(url)
    if p.scheme or p.netloc or url.startswith("//") or not url.startswith("/"):
        return fallback
    return url


# ---- Login brute-force throttle (simple in-memory, per worker) ----
import time
_LOGIN_THROTTLE = {}  # ip -> [fail_count, window_start]


def _throttle_check(ip, max_tries=5, window=300):
    """False = block karo. Note: in-memory hai, isliye har gunicorn worker
    apna count rakhta hai — chhote scale par kaafi hai."""
    now = time.time()
    rec = _LOGIN_THROTTLE.get(ip)
    if rec is None or now - rec[1] > window:
        rec = [0, now]
        _LOGIN_THROTTLE[ip] = rec
    if rec[0] >= max_tries:
        return False
    rec[0] += 1
    return True

# Reload fix: ensure fresh content on every load (no stale cache)
# + security headers har response par
@app.after_request
def add_no_cache_headers(resp):
    if request.path.startswith("/static/"):
        # static files: short cache (CSS versioning handles busting)
        resp.headers["Cache-Control"] = "public, max-age=300"
    else:
        # HTML pages: always fresh
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
    for k, v in _SECURITY_HEADERS.items():
        resp.headers[k] = v
    # C7: note content par extra-strict CSP — yahan scripts bilkul nahi
    # (sandbox ke saath double cover)
    if request.path.endswith("/view/content"):
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'none'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; font-src 'self' data:; "
            "frame-ancestors 'self'; base-uri 'none'"
        )
    return resp

for folder in (PDF_FOLDER, HTML_FOLDER, UPI_FOLDER):
    os.makedirs(folder, exist_ok=True)


# ============================================================
# DATABASE HELPERS
# ============================================================
def get_db():
    # M6: timeout + busy_timeout — gunicorn multi-worker concurrency ke liye
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db():
    conn = get_db()
    # M6: WAL mode — concurrent read/write safe (har deploy par ek baar set hota hai)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            hindi TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject_slug TEXT NOT NULL,
            description TEXT DEFAULT '',
            price REAL NOT NULL DEFAULT 0,
            original_price REAL,
            file_type TEXT NOT NULL,      -- pdf / html
            file_path TEXT NOT NULL,
            original_name TEXT DEFAULT '',
            pages INTEGER,
            language TEXT DEFAULT 'Hindi + English',
            featured INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (subject_slug) REFERENCES subjects(slug)
        );
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER,
            payment_id TEXT,
            order_id TEXT,
            amount REAL,
            status TEXT,
            email TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bundle_id INTEGER,
            email TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS admin_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            detail TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
    """)
    # M6: Indexes — har request ke queries (subject filter, sort, purchase lookups)
    conn.executescript("""
        CREATE INDEX IF NOT EXISTS idx_notes_subject ON notes(subject_slug);
        CREATE INDEX IF NOT EXISTS idx_notes_created ON notes(created_at);
        CREATE INDEX IF NOT EXISTS idx_notes_featured ON notes(featured);
        CREATE INDEX IF NOT EXISTS idx_payments_pid ON payments(payment_id);
        CREATE INDEX IF NOT EXISTS idx_purchases_user_bundle ON purchases(user_id, bundle_id);
    """)
    # seed subjects if empty
    count = conn.execute("SELECT COUNT(*) AS c FROM subjects").fetchone()["c"]
    if count == 0:
        for s in DEFAULT_SUBJECTS:
            conn.execute(
                "INSERT INTO subjects (slug, name, hindi) VALUES (?, ?, ?)",
                (s["slug"], s["name"], s["hindi"]),
            )
    conn.commit()
    conn.close()


init_db()


# M5: Subjects list har request par DB se nahi — 60s TTL cache
# (subject add/delete hone ke 60s baad fresh dikhegi — kaafi hai)
_subjects_cache = {"rows": None, "ts": 0}


def get_subjects():
    if _subjects_cache["rows"] is None or time.time() - _subjects_cache["ts"] > 60:
        conn = get_db()
        rows = conn.execute("SELECT * FROM subjects ORDER BY id").fetchall()
        conn.close()
        _subjects_cache["rows"] = [dict(r) for r in rows]
        _subjects_cache["ts"] = time.time()
    return _subjects_cache["rows"]


def invalidate_subjects_cache():
    _subjects_cache["rows"] = None
    _subjects_cache["ts"] = 0


def get_subject(slug):
    conn = get_db()
    row = conn.execute("SELECT * FROM subjects WHERE slug=?", (slug,)).fetchone()
    conn.close()
    return dict(row) if row else None


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ext(filename):
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def get_note_content(row):
    """Note ka content nikaalo — compressed hai toh decompress karo."""
    content = row["content"]
    if not content and row["content_compressed"]:
        try:
            import gzip
            content = gzip.decompress(row["content_compressed"]).decode("utf-8")
        except Exception:
            content = ""
    return content


def clean_note_html(content):
    """Preview ke liye note HTML ko clean karo:
       - external font @import / @font-face hatao (network ke bina bhi render ho)
       - system Devanagari font fallback lagao taaki Hindi text hamesha dikhe
       - koi 'file://' path hatao"""
    import re
    # remove @import statements (external fonts/CSS)
    content = re.sub(r"@import[^;]*;", "", content)
    # remove @font-face blocks
    content = re.sub(r"@font-face\s*\{[^}]*\}", "", content, flags=re.S)
    # remove any file:// references
    content = content.replace("file://", "")
    # Devanagari-friendly font fallback add karo body/html par (agar set nahi hai)
    font_stack = ("'Noto Sans Devanagari', 'Mangal', 'Nirmala UI', "
                  "'Segoe UI', 'Arial Unicode MS', sans-serif")
    # add global font-family rule if there's a <style>
    if "<style" in content.lower():
        content = content.replace(
            "</style>",
            "body{font-family:%s} </style>" % font_stack,
            1,
        )
    return content


MOBILE_RESPONSIVE_CSS = (
    "html,body{max-width:100% !important;width:100% !important;margin:0 auto !important;}"
    "body{word-wrap:break-word !important;overflow-wrap:break-word !important;"
    "padding:12px !important;box-sizing:border-box !important;font-size:16px !important;}"
    "img{max-width:100% !important;height:auto !important;}"
    "table{max-width:100% !important;width:100% !important;table-layout:auto;border-collapse:collapse;}"
    "table td,table th{padding:6px !important;word-wrap:break-word !important;overflow-wrap:break-word !important;}"
    "table,tr,td,th{min-width:0 !important;}"
    ".table-wrap{max-width:100%;overflow-x:auto;}"
    "pre,code{white-space:pre-wrap !important;word-wrap:break-word !important;}"
    "h1,h2,h3,h4,h5,p,li,div{word-wrap:break-word;overflow-wrap:break-word;max-width:100%;}"
    "*{box-sizing:border-box;}"
)


def make_mobile_responsive(content):
    """Note HTML me viewport meta + mobile-responsive CSS inject karo,
    taaki mobile pe text scatter na ho / overflow na ho.
    Agar content mein head na ho toh poora responsive wrapper bana do."""
    if not content:
        return content
    viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    style = "<style>%s</style>" % MOBILE_RESPONSIVE_CSS
    lower = content.lower()
    if "</head>" in lower:
        return content.replace(
            "</head>",
            viewport + "\n" + style + "\n</head>",
            1,
        )
    if "<head" in lower:
        # head tag hai par closing nahi — style sabse upar daalo
        idx = content.lower().find("<head")
        end = content.find(">", idx) + 1
        return content[:end] + viewport + style + content[end:]
    if "<body" in lower:
        return viewport + style + content
    # bilkul plain text/none-HTML — wrapper banao
    return (f"<!DOCTYPE html><html><head>{viewport}{style}</head>"
            f"<body>{content}</body></html>")


def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return f(*args, **kwargs)
    return wrapper


SUBJECT_EMOJI = {
    "geography": "🌍", "polity": "🏛️", "economics": "📈", "history": "🏺",
    "science-tech": "🔬", "environment": "🌿", "art-culture": "🎭",
    "current-affairs": "📰", "ethics": "⚖️", "ir": "🌐",
    "internal-security": "🛡️", "indian-society": "👥", "csat": "🧮",
    "prelims": "🎯", "mains": "✍️", "other": "📚", "pyqs": "📝",
    "geomorphology": "⛰️", "climatology": "🌦️", "oceanography": "🌊",
    "indian-physiography": "🏞️", "mapping": "🗺️",
    "geography-optional": "🗺️",
    "ancient-history": "🏺", "medieval-history": "🏰", "modern-history": "🏛️",
    "post-independence": "🇮🇳", "world-history": "🌍",
}

# Har subject ka EK preview note (demo) — DB se dynamic compute hota hai
# (har subject mein sabse chhota id wala non-bundle note). Sirf ye preview mein khulega, baaki locked.
def _compute_demo_preview_ids():
    ids = set()
    try:
        conn = get_db()
        rows = conn.execute(
            """SELECT n.id, n.subject_slug FROM notes n
               WHERE n.id = (
                   SELECT n2.id FROM notes n2
                   WHERE n2.subject_slug = n.subject_slug
                     AND n2.title NOT LIKE '%Complete Bundle%'
                   ORDER BY n2.id LIMIT 1
               )
               UNION
               -- subjects jisme sirf bundle hai (fallback: sabse chhota note)
               SELECT n3.id, n3.subject_slug FROM notes n3
               WHERE n3.subject_slug NOT IN (
                   SELECT DISTINCT subject_slug FROM notes WHERE title NOT LIKE '%Complete Bundle%'
               )
               GROUP BY n3.subject_slug HAVING n3.id = MIN(n3.id)"""
        ).fetchall()
        conn.close()
        for r in rows:
            ids.add(r["id"])
    except Exception:
        pass
    return ids


# M4: Pehle ye import-time par ek baar compute hota tha (naye notes par stale
# rehta). Ab 60s ka TTL cache — har 60s mein fresh, par har request par nahi.
_demo_preview_cache = {"ids": None, "ts": 0}


def demo_preview_ids():
    if _demo_preview_cache["ids"] is None or time.time() - _demo_preview_cache["ts"] > 60:
        _demo_preview_cache["ids"] = _compute_demo_preview_ids()
        _demo_preview_cache["ts"] = time.time()
    return _demo_preview_cache["ids"]


def _check_view_access(note, conn):
    """Individual note ka view access: admin / free subject / demo preview /
    purchased subject bundle. (note_view + note_view_content dono use karte hain)"""
    if session.get("is_admin"):
        return True
    # FREE subjects — in subjects ke notes bina login/payment ke khulte hain
    if note["subject_slug"] in FREE_SUBJECTS:
        return True
    if note["id"] in demo_preview_ids():
        return True
    if session.get("user_id"):
        # kya user ne is subject ka bundle kharida hai?
        bought = conn.execute(
            "SELECT id FROM purchases WHERE user_id=? AND bundle_id IN "
            "(SELECT id FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%')",
            (session["user_id"], note["subject_slug"])).fetchone()
        return bool(bought)
    return False


def subject_emoji(slug):
    return SUBJECT_EMOJI.get(slug, "📚")


def subject_name(slug):
    subj = get_subject(slug)
    return subj["name"] if subj else slug


@app.context_processor
def inject_globals():
    def with_emoji(subjects):
        out = []
        for s in subjects:
            s = dict(s)
            s["emoji"] = subject_emoji(s["slug"])
            out.append(s)
        return out

    return {
        "SITE_NAME": SITE_NAME,
        "SITE_TAGLINE": SITE_TAGLINE,
        "all_subjects": with_emoji(get_subjects()),
        "is_admin": bool(session.get("is_admin")),
        "now_year": lambda: datetime.now().year,
        "subject_emoji": subject_emoji,
        "subject_name": subject_name,
        "demo_preview_ids": demo_preview_ids(),
        "current_user": session.get("user_name"),
        "is_user": bool(session.get("user_id")),
    }


# ============================================================
# PUBLIC ROUTES
# ============================================================
@app.route("/")
def index():
    conn = get_db()
    featured = conn.execute(
        "SELECT * FROM notes WHERE featured=1 ORDER BY created_at DESC LIMIT 6"
    ).fetchall()
    featured_ids = [r["id"] for r in featured]
    # Recent mein wo notes NAHI jo featured mein already hain (duplicate hatao)
    if featured_ids:
        placeholders = ",".join("?" * len(featured_ids))
        recent = conn.execute(
            f"SELECT * FROM notes WHERE id NOT IN ({placeholders}) ORDER BY created_at DESC LIMIT 9",
            featured_ids,
        ).fetchall()
    else:
        recent = conn.execute(
            "SELECT * FROM notes ORDER BY created_at DESC LIMIT 9"
        ).fetchall()
    subject_counts = conn.execute(
        """SELECT s.slug, s.name, s.hindi, COUNT(n.id) AS cnt
           FROM subjects s LEFT JOIN notes n ON n.subject_slug = s.slug
           GROUP BY s.id ORDER BY s.id"""
    ).fetchall()
    total_notes = conn.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    bundle_count = conn.execute("SELECT COUNT(*) AS c FROM notes WHERE featured=1").fetchone()["c"]
    # Geography/History ke parts ko home grid se chhupao (wo parent ke andar dikhenge)
    child_slugs = set()
    for children in CHILD_SUBJECTS.values():
        child_slugs.update(children)
    # Home grid se chhupao: parts, optional, aur prelims/mains/other (PYQs section alag dikhega)
    hidden_slugs = {"geography-optional", "prelims", "mains", "other"}
    subject_counts = [dict(r) for r in subject_counts
                      if r["slug"] not in child_slugs and r["slug"] not in hidden_slugs]
    # M5: har subject ka bundle — PEHLE ek query per subject hota tha (N+1),
    # ab poore bundles EK query mein fetch karo
    bundles = {}
    for b in conn.execute(
        "SELECT subject_slug, id, price, original_price FROM notes WHERE title LIKE '%Complete Bundle%'"
    ).fetchall():
        bundles[b["subject_slug"]] = b
    for sc in subject_counts:
        b = bundles.get(sc["slug"])
        sc["bundle_id"] = b["id"] if b else None
        sc["bundle_price"] = b["price"] if b else 0
        sc["bundle_orig"] = b["original_price"] if b else 0
    conn.close()
    return render_template(
        "index.html",
        featured=[dict(n) for n in featured],
        recent=[dict(n) for n in recent],
        subject_counts=subject_counts,
        total_notes=total_notes,
        bundle_count=bundle_count,
        subject_count=len(subject_counts),
    )


@app.route("/notes")
def browse():
    q = request.args.get("q", "").strip()
    subject = request.args.get("subject", "").strip()
    sort = request.args.get("sort", "new")
    conn = get_db()
    sql = "SELECT * FROM notes WHERE 1=1"
    params = []
    if q:
        sql += " AND (title LIKE ? OR description LIKE ?)"
        like = f"%{q}%"
        params += [like, like]
    if subject:
        sql += " AND subject_slug=?"
        params.append(subject)
    if sort == "price_low":
        sql += " ORDER BY price ASC"
    elif sort == "price_high":
        sql += " ORDER BY price DESC"
    else:
        sql += " ORDER BY created_at DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template(
        "browse.html",
        notes=[dict(n) for n in rows],
        q=q, subject=subject, sort=sort,
    )


# Har subject ke child/up-parts
CHILD_SUBJECTS = {
    "geography": ["geomorphology", "climatology", "oceanography", "indian-physiography", "mapping"],
    "history": ["ancient-history", "medieval-history", "modern-history", "post-independence", "world-history"],
}


@app.route("/subject/<slug>")
def subject_page(slug):
    subj = get_subject(slug)
    if not subj:
        abort(404)
    conn = get_db()
    # Subject page par SIRF bundle dikhayein, individual files nahi
    rows = conn.execute(
        "SELECT * FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%' ORDER BY created_at DESC",
        (slug,),
    ).fetchall()
    # PYQs subject — saare papers year-wise dikhao (individual notes)
    pyq_notes = []
    if slug == "pyqs":
        pyq_notes = [dict(r) for r in conn.execute(
            "SELECT * FROM notes WHERE subject_slug='pyqs' AND title NOT LIKE '%Complete Bundle%' ORDER BY title"
        ).fetchall()]
    # Current Affairs subject — saare months dikhao (individual notes)
    ca_notes = []
    if slug == "current-affairs":
        ca_notes = [dict(r) for r in conn.execute(
            "SELECT * FROM notes WHERE subject_slug='current-affairs' AND title NOT LIKE '%Complete Bundle%' ORDER BY title"
        ).fetchall()]
    # child subjects (sub-parts) fetch karo — har part ki bundle/price info ke saath
    children = []
    for cslug in CHILD_SUBJECTS.get(slug, []):
        c = get_subject(cslug)
        if c:
            c_count = conn.execute("SELECT COUNT(*) AS c FROM notes WHERE subject_slug=?", (cslug,)).fetchone()["c"]
            c = dict(c)
            c["count"] = c_count
            # part ka bundle (agar hai) — price + preview/buy ke liye
            part_bundle = conn.execute(
                "SELECT id, price, original_price FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%' LIMIT 1",
                (cslug,)).fetchone()
            c["bundle_id"] = part_bundle["id"] if part_bundle else None
            c["price"] = part_bundle["price"] if part_bundle else 0
            c["orig_price"] = part_bundle["original_price"] if part_bundle else 0
            # part ki pehli file id — preview click par seedhi HTML file khule
            first_file = conn.execute(
                "SELECT id FROM notes WHERE subject_slug=? AND title NOT LIKE '%Complete Bundle%' ORDER BY id LIMIT 1",
                (cslug,)).fetchone()
            c["first_file_id"] = first_file["id"] if first_file else None
            children.append(c)
    conn.close()
    # PYQs papers ko Prelims/Mains me split karo (template me aasan dikhane ke liye)
    pyq_prelims = [n for n in pyq_notes if "Prelims" in (n["title"] or "")]
    pyq_mains = [n for n in pyq_notes if "Mains" in (n["title"] or "")]
    # Current Affairs months ko month-order me sort karo
    month_order = ["January","February","March","April","May","June","July",
                   "August","September","October","November","December"]
    ca_sorted = sorted(ca_notes, key=lambda n: month_order.index(next((m for m in month_order if m in (n["title"] or "")), "January")))
    return render_template("subject.html", subject=subj, notes=[dict(n) for n in rows], children=children,
                           pyq_notes=pyq_notes, pyq_prelims=pyq_prelims, pyq_mains=pyq_mains,
                           ca_notes=ca_sorted)


@app.route("/note/<int:note_id>")
def note_detail(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
    return render_template("note_detail.html", note=note)


@app.route("/note/<int:note_id>/view")
def note_view(note_id):
    """Preview:
    - Bundle → ek page jisme subject ke saare topics ki list + pehli file ka content dikhta hai.
    - Individual HTML files → sandboxed iframe wrapper (scripts block — C7 fix).
    - Individual PDF → direct inline.
    Download alag se locked hai."""
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        abort(404)
    note = dict(row)
    is_bundle = "Complete Bundle" in (note["title"] or "")
    # Kya user ne ye bundle buy kiya hai? (admin ko bhi free access)
    purchased = False
    if is_bundle:
        if session.get("is_admin"):
            purchased = True
        elif session.get("user_id"):
            p = conn.execute("SELECT id FROM purchases WHERE user_id=? AND bundle_id=?",
                             (session["user_id"], note_id)).fetchone()
            purchased = bool(p)
    # Bundle preview → topics list + pehli file ka content
    if is_bundle:
        # child parts (jaise history ke 5 parts, geography ke parts)
        child_parts = []
        for cslug in CHILD_SUBJECTS.get(note["subject_slug"], []):
            c = get_subject(cslug)
            if c:
                cfiles = [dict(r) for r in conn.execute(
                    "SELECT * FROM notes WHERE subject_slug=? AND title NOT LIKE '%Complete Bundle%' ORDER BY id LIMIT 1",
                    (cslug,)).fetchall()]
                c = dict(c)
                c["count"] = conn.execute("SELECT COUNT(*) c FROM notes WHERE subject_slug=?", (cslug,)).fetchone()["c"]
                if cfiles:
                    pf = cfiles[0]
                    import base64
                    pf["content"] = base64.b64encode(
                        (make_mobile_responsive(get_note_content(pf) or "") or "").encode("utf-8")
                    ).decode()
                    c["preview_file"] = pf
                else:
                    c["preview_file"] = None
                child_parts.append(c)
        # is bundle ke subject ke saare individual notes (topics)
        topics = [dict(r) for r in conn.execute(
            "SELECT id, title FROM notes WHERE subject_slug=? AND title NOT LIKE '%Complete Bundle%' ORDER BY id",
            (note["subject_slug"],)
        ).fetchall()]
        # pehli file ka content (base64 mein — iframe srcdoc blank issue se bachne ke liye)
        first_content = ""
        import base64
        if topics:
            first_row = conn.execute("SELECT * FROM notes WHERE id=?",
                                     (topics[0]["id"],)).fetchone()
            if first_row:
                raw = make_mobile_responsive(get_note_content(dict(first_row)) or "") or ""
                first_content = base64.b64encode(raw.encode("utf-8")).decode()
        elif child_parts and child_parts[0]["preview_file"]:
            raw = make_mobile_responsive(get_note_content(child_parts[0]["preview_file"])) or ""
            first_content = base64.b64encode(raw.encode("utf-8")).decode()
        conn.close()
        return render_template("preview.html", bundle=note, topics=topics, first_content=first_content, purchased=purchased, child_parts=child_parts)
    # Individual → demo ids OR purchased subject ke notes khule
    if not _check_view_access(note, conn):
        conn.close()
        return redirect(url_for("buy_note", note_id=note_id))
    content = get_note_content(note)
    conn.close()
    if note["file_type"] == "html" and content:
        # C7: content ko sandboxed iframe wrapper ke andar serve karo (scripts block)
        return render_template("note_view_wrapper.html", note=note)
    full = os.path.join(BASE_DIR, note["file_path"])
    if not os.path.exists(full):
        abort(404)
    folder = os.path.dirname(full)
    name = os.path.basename(full)
    return send_from_directory(folder, name, as_attachment=False)


@app.route("/note/<int:note_id>/view/content")
def note_view_content(note_id):
    """Note ka raw HTML — sirf wrapper ke SANDBOXED iframe ke liye (C7).

    Security: (1) access check /view jaisa hi, (2) iframe par `sandbox` hai
    isliye note mein koi bhi <script>/on* handler execute NAHI hota,
    (3) is path par CSP `script-src 'none'` hai (after_request mein)."""
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        abort(404)
    note = dict(row)
    if note["file_type"] != "html":
        conn.close()
        abort(404)
    if not _check_view_access(note, conn):
        conn.close()
        return redirect(url_for("buy_note", note_id=note_id))
    content = get_note_content(note)
    conn.close()
    if not content:
        abort(404)
    return Response(make_mobile_responsive(clean_note_html(content)) or "",
                    mimetype="text/html")


@app.route("/library/<int:bundle_id>")
def library(bundle_id):
    """Purchased bundle — saari files chapter-wise. Sirf paid user/admin."""
    conn = get_db()
    bundle = conn.execute("SELECT * FROM notes WHERE id=? AND title LIKE '%Complete Bundle%'", (bundle_id,)).fetchone()
    if not bundle:
        conn.close()
        abort(404)
    has_access = session.get("is_admin")
    if not has_access and session.get("user_id"):
        p = conn.execute("SELECT id FROM purchases WHERE user_id=? AND bundle_id=?", (session["user_id"], bundle_id)).fetchone()
        has_access = bool(p)
    if not has_access:
        conn.close()
        return redirect(url_for("buy_note", note_id=bundle_id))
    # bundle ke subject ke saari individual files
    files = [dict(r) for r in conn.execute(
        "SELECT * FROM notes WHERE subject_slug=? AND title NOT LIKE '%Complete Bundle%' ORDER BY id",
        (bundle["subject_slug"],)
    ).fetchall()]
    conn.close()
    return render_template("library.html", bundle=dict(bundle), files=files)


@app.route("/download/<int:note_id>")
def download_note(note_id):
    """Download LOCKED — sirf admin/paid customer (jisne bundle kharida) hi download kar sakta hai."""
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        abort(404)
    note = dict(row)
    has_access = session.get("is_admin")
    # FREE subjects — in subjects ke notes bina login/payment ke download ho sakte hain
    if note["subject_slug"] in FREE_SUBJECTS:
        has_access = True
    if not has_access and session.get("user_id"):
        bought = conn.execute(
            "SELECT id FROM purchases WHERE user_id=? AND bundle_id IN "
            "(SELECT id FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%')",
            (session["user_id"], note["subject_slug"])).fetchone()
        has_access = bool(bought)
    conn.close()
    if not has_access:
        return redirect(url_for("buy_note", note_id=note_id))
    # DB content se download (html) — reliable (compressed bhi handle karo)
    content = get_note_content(note)
    if note["file_type"] == "html" and content:
        dl_name = note["original_name"] or f"note-{note_id}.html"
        return Response(
            clean_note_html(content),
            mimetype="text/html",
            headers={"Content-Disposition": f'attachment; filename="{dl_name}"'},
        )
    full = os.path.join(BASE_DIR, note["file_path"])
    if not os.path.exists(full):
        abort(404)
    folder = os.path.dirname(full)
    name = os.path.basename(full)
    # download with original name if pdf
    dl_name = note["original_name"] if note["original_name"] else name
    return send_from_directory(folder, name, as_attachment=True, download_name=dl_name)


@app.route("/buy/<int:note_id>")
def buy_note(note_id):
    # Buy karne ke liye user ko login/signup karna padega (purchase account mein save hota hai)
    if not session.get("user_id"):
        return redirect(url_for("login", next=url_for("buy_note", note_id=note_id)))
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
    is_free = note["subject_slug"] in FREE_SUBJECTS
    # Agar free note hai toh user ko directly download/view ka option do (payment nahi)
    if is_free:
        return redirect(url_for("note_view", note_id=note_id))
    # QR: embedded base64 se data-URI banate hain (file ki zaroorat nahi)
    qr = "data:image/png;base64," + UPI_QR_BASE64
    return render_template(
        "buy.html",
        note=note,
        qr=qr,
        UPI_ID=UPI_ID,
        SELLER_PHONE=SELLER_PHONE,
        SELLER_WHATSAPP=SELLER_WHATSAPP,
        SELLER_EMAIL=SELLER_EMAIL,
    )


@app.route("/uploads/upi/<path:filename>")
def upi_qr(filename="qr.png"):
    return send_from_directory(UPI_FOLDER, filename)


# ============================================================
# RAZORPAY PAYMENT ROUTES (Test Mode)
# ============================================================
def _get_razorpay_client():
    if not _razorpay_available or not RAZORPAY_KEY_SECRET:
        return None
    return razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route("/pay/<int:note_id>")
def pay_order(note_id):
    """Razorpay order create karo.

    SECURITY: order ke 'notes' field mein note_id + amount_paise store karte
    hain. Ye Razorpay ke paas (server-side) rehta hai, isliye verify par
    note ka pata sirf order se hi chalega — client-side form wala note_id
    par bharosa NAHI karna (pehle se wahi bug tha: ₹49 payment karke ₹499
    bundle ka note_id bhej ke access le liya ja sakta tha)."""
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
    client = _get_razorpay_client()
    if client is None:
        flash("Razorpay configured nahi hai (Key Secret missing).", "error")
        return redirect(url_for("buy_note", note_id=note_id))
    if note["price"] <= 0:
        flash("Ye note free hai — direct download/view karein.", "info")
        return redirect(url_for("note_view", note_id=note_id))
    amount_paise = int(round(note["price"] * 100))
    try:
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"note_{note_id}",
            "payment_capture": 1,
            # Server-side binding: verify par order se hi note_id nikalega
            "notes": {"note_id": str(note_id), "amount_paise": str(amount_paise)},
        })
    except Exception as e:
        flash(f"Order create error: {e}", "error")
        return redirect(url_for("buy_note", note_id=note_id))
    return render_template(
        "pay.html",
        note=note,
        order=order,
        key_id=RAZORPAY_KEY_ID,
        RAZORPAY_TEST_MODE=True,
    )


@app.route("/pay/verify", methods=["POST"])
def pay_verify():
    """Razorpay payment verify karo — secure flow:

    1. Signature verify (order_id + payment_id + HMAC).
    2. Order Razorpay se FETCH karke uske `notes` se note_id nikaalo.
       (Client-side form mein bheja gaya note_id IGNORE hota hai.)
    3. Order ka amount == order-time par recorded amount hona chahiye
       (legacy orders ke liye: note ki current price).
    4. Order status 'paid' hona chahiye.
    5. Replay protection: same payment_id dobara process nahi hota,
       purchase insert idempotent hai (double grant nahi hoga).
    """
    import json
    import re
    params = request.form.to_dict()
    client = _get_razorpay_client()
    if client is None:
        flash("Payment verify nahi ho sakta (Razorpay configured nahi hai).", "error")
        return redirect(url_for("index"))

    order_id = params.get("razorpay_order_id", "")
    payment_id = params.get("razorpay_payment_id", "")
    if not order_id or not payment_id:
        flash("Payment verify fail — details missing hain.", "error")
        return redirect(url_for("index"))

    # 1) Signature verify (SDK False return kar sakta hai ya exception — dono handle)
    try:
        sig_ok = client.utility.verify_payment_signature(params)
    except Exception:
        sig_ok = False
    if not sig_ok:
        flash("Payment verify fail — signature match nahi hua.", "error")
        return redirect(url_for("index"))

    # 2) Order fetch — note_id sirf Razorpay ke order se hi
    try:
        order = client.order.fetch(order_id)
    except Exception:
        flash("Order fetch fail — dobara try karein.", "error")
        return redirect(url_for("index"))

    if order.get("status") != "paid":
        flash("Payment abhi confirmed nahi hui.", "error")
        return redirect(url_for("index"))
    # Extra sanity: order ka payment_id form wale se match kare
    if order.get("payment_id") and order.get("payment_id") != payment_id:
        flash("Payment verify fail — order/payment mismatch.", "error")
        return redirect(url_for("index"))

    notes = order.get("notes") or {}
    if isinstance(notes, str):
        try:
            notes = json.loads(notes)
        except Exception:
            notes = {}
    try:
        note_id = int(notes["note_id"])
        order_paise_recorded = int(notes["amount_paise"])
    except (KeyError, TypeError, ValueError):
        # Legacy order (is fix se pehle bana) — receipt "note_<id>" se fallback
        m = re.match(r"^note_(\d+)$", order.get("receipt") or "")
        if not m:
            flash("Order ko kisi note se match nahi kiya ja saka.", "error")
            return redirect(url_for("index"))
        note_id = int(m.group(1))
        order_paise_recorded = None

    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        conn.close()
        flash("Note nahi mila.", "error")
        return redirect(url_for("index"))
    note = dict(row)

    # 3) Amount check — jo paisa laga, wahi order mein recorded tha
    if order_paise_recorded is not None:
        # Naya order: order-time par site jis price par bola tha, wahi charge hua
        # (baad mein price change ho toh bhi order-time price hi authoritative hai)
        if int(order.get("amount", 0)) != order_paise_recorded:
            flash("Payment amount mismatch — dobara try karein.", "error")
            conn.close()
            return redirect(url_for("index"))
    else:
        # Legacy order: note ki current price se match karo
        if int(order.get("amount", 0)) != int(round(note["price"] * 100)):
            flash("Payment amount note price se match nahi karta.", "error")
            conn.close()
            return redirect(url_for("index"))

    # User ka email (payments record ke liye)
    email = ""
    if session.get("user_id"):
        u = conn.execute("SELECT email FROM users WHERE id=?", (session["user_id"],)).fetchone()
        if u:
            email = u["email"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 5) Replay protection + idempotent inserts
    already = conn.execute("SELECT id FROM payments WHERE payment_id=?", (payment_id,)).fetchone()
    if not already:
        conn.execute(
            "INSERT INTO payments (note_id, payment_id, order_id, amount, status, email, created_at) VALUES (?,?,?,?,?,?,?)",
            (note["id"], payment_id, order_id, note["price"], "paid", email, now),
        )
    if session.get("user_id"):
        p = conn.execute("SELECT id FROM purchases WHERE user_id=? AND bundle_id=?",
                         (session["user_id"], note["id"])).fetchone()
        if not p:
            conn.execute(
                "INSERT INTO purchases (user_id, bundle_id, email, created_at) VALUES (?,?,?,?)",
                (session["user_id"], note["id"], email, now),
            )
    conn.commit()
    conn.close()

    flash("Payment successful! ✅ Bundle unlock ho gaya — Library se kholen.", "success")
    return redirect(url_for("buy_success", note_id=note["id"], payment_id=payment_id))


@app.route("/buy/success/<int:note_id>")
def buy_success(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    note = dict(row) if row else None
    return render_template("buy_success.html", note=note, payment_id=request.args.get("payment_id"))


@app.route("/google33ceddf537433e15.html")
def google_verify():
    return Response(
        "google-site-verification: google33ceddf537433e15.html",
        mimetype="text/html",
    )


@app.route("/robots.txt")
def robots_txt():
    content = "User-agent: *\nAllow: /\nSitemap: " + request.url_root.rstrip("/") + "/sitemap.xml\n"
    return Response(content, mimetype="text/plain")


# M12: Sitemap — pehle har hit par saari notes query + sabka lastmod = aaj ki
# date. Ab 1-hour cache + asli lastmod (note ki created_at).
_sitemap_cache = {"body": None, "ts": 0}


def _build_sitemap():
    conn = get_db()
    base = request.url_root.rstrip("/")
    urls = [(base + "/", datetime.now().strftime("%Y-%m-%d"))]
    for r in conn.execute("SELECT id, created_at FROM notes"):
        urls.append((f"{base}/note/{r['id']}", (r["created_at"] or "")[:10] or datetime.now().strftime("%Y-%m-%d")))
    for r in conn.execute("SELECT slug FROM subjects"):
        urls.append((f"{base}/subject/{r['slug']}", datetime.now().strftime("%Y-%m-%d")))
    conn.close()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lastmod in urls:
        xml.append(f'<url><loc>{u}</loc><lastmod>{lastmod}</lastmod><changefreq>weekly</changefreq></url>')
    xml.append('</urlset>')
    return "\n".join(xml)


@app.route("/sitemap.xml")
def sitemap_xml():
    if _sitemap_cache["body"] is None or time.time() - _sitemap_cache["ts"] > 3600:
        _sitemap_cache["body"] = _build_sitemap()
        _sitemap_cache["ts"] = time.time()
    return Response(_sitemap_cache["body"], mimetype="application/xml")


@app.route(ADMIN_PREFIX + "/manifest.json")
@login_required
def admin_manifest():
    """PWA manifest — admin app ko phone pe install karne ke liye.

    SECURITY: Pehle ye root par public tha aur ADMIN_PREFIX (secret token)
    expose karta tha. Ab sirf admin prefix ke neeche + login ke saath."""
    data = {
        "name": "ANUJ Admin — UPSC Notes Store",
        "short_name": "ANUJ Admin",
        "description": "Admin app for ANUJ IAS ASPIRANT",
        "start_url": ADMIN_PREFIX + "/",
        "scope": ADMIN_PREFIX + "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#2d0d66",
        "theme_color": "#2d0d66",
        "icons": [
            {"src": url_for("static", filename="aw-logo-192.png"),
             "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": url_for("static", filename="aw-logo-512.png"),
             "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    import json
    return Response(json.dumps(data), mimetype="application/manifest+json")


@app.route(ADMIN_PREFIX + "/service-worker.js")
@login_required
def admin_sw():
    """Simple service worker — admin app offline-cache ke liye.

    SECURITY: Pehle root par public tha (token SCOPE constant mein tha).
    Ab sirf admin prefix ke neeche + login ke saath."""
    scope = ADMIN_PREFIX + "/"
    js = (
        "const CACHE='anuj-admin-v1';\n"
        "const SCOPE='" + scope + "';\n"
        "self.addEventListener('install',e=>{self.skipWaiting();});\n"
        "self.addEventListener('activate',e=>{e.waitUntil(clients.claim());});\n"
        "self.addEventListener('fetch',e=>{\n"
        "  const req=e.request;\n"
        "  if(req.method!=='GET')return;\n"
        "  const url=new URL(req.url);\n"
        "  if(url.pathname.startsWith(SCOPE) || url.pathname.includes('/static/')){\n"
        "    e.respondWith(fetch(req).then(res=>{\n"
        "      const copy=res.clone();\n"
        "      caches.open(CACHE).then(c=>c.put(req,copy));\n"
        "      return res;\n"
        "    }).catch(()=>caches.match(req)));\n"
        "  }\n"
        "});\n"
    )
    return Response(js, mimetype="application/javascript")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html",
                           SELLER_EMAIL=SELLER_EMAIL,
                           SELLER_WHATSAPP=SELLER_WHATSAPP)


# ============================================================
# USER ROUTES (Login / Signup / Dashboard)
# ============================================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    next_url = safe_next(request.args.get("next") or request.form.get("next"), url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not name or not email or not password:
            flash("Naam, email aur password sab zaroori hai.", "error")
            return redirect(url_for("signup", next=next_url))
        if password != confirm:
            flash("Password aur confirm password match nahi karte.", "error")
            return redirect(url_for("signup", next=next_url))
        if len(password) < 8:
            flash("Password kam se kam 8 characters ka rakhein.", "error")
            return redirect(url_for("signup", next=next_url))
        conn = get_db()
        exists = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if exists:
            conn.close()
            flash("Is email se account pehle se hai. Login karein.", "error")
            return redirect(url_for("login", next=next_url))
        conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?,?,?,?)",
            (name, email, generate_password_hash(password), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome, {name}! 🎉 Account ban gaya.", "success")
        return redirect(next_url)
    return render_template("signup.html", next_url=next_url)


@app.route("/login", methods=["GET", "POST"])
def login():
    next_url = safe_next(request.args.get("next") or request.form.get("next"), url_for("index"))
    if request.method == "POST":
        ip = request.remote_addr or "?"
        if not _throttle_check(ip):
            flash("Bahut saari galat koshishen ho gayi hain. 5 minute baad try karein.", "error")
            return render_template("login.html", next_url=next_url)
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            _LOGIN_THROTTLE.pop(ip, None)
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}! 👋", "success")
            return redirect(next_url)
        flash("Galat email ya password!", "error")
    return render_template("login.html", next_url=next_url)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    flash("Aap logout ho gaye.", "info")
    return redirect(url_for("index"))


@app.route("/account")
def user_dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
    conn.close()
    return render_template("account.html", user=dict(user) if user else None)


# ============================================================
# ADMIN ROUTES
# ============================================================
@app.route(ADMIN_PREFIX + "/login", methods=["GET", "POST"])
def admin_login():
    next_url = safe_next(request.args.get("next"), url_for("admin_dashboard"))
    if request.method == "POST":
        ip = request.remote_addr or "?"
        if not _throttle_check(ip, max_tries=5, window=600):
            flash("Bahut saari galat koshishen ho gayi hain. 10 minute baad try karein.", "error")
            return render_template("admin_login.html")
        # timing-attack safe compare (plaintext equality ki jagah)
        username_ok = secrets.compare_digest(request.form.get("username", ""), ADMIN_USERNAME)
        password_ok = secrets.compare_digest(request.form.get("password", ""), ADMIN_PASSWORD)
        if username_ok and password_ok:
            _LOGIN_THROTTLE.pop(ip, None)
            session["is_admin"] = True
            flash("Welcome back, Admin! 👋", "success")
            return redirect(next_url)
        flash("Galat username ya password! ❌", "error")
    return render_template("admin_login.html")


@app.route(ADMIN_PREFIX + "/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Aap logout ho gaye hain.", "info")
    return redirect(url_for("index"))


@app.route(ADMIN_PREFIX + "/")
def admin_dashboard_slash():
    # Trailing-slash variant — dashboard par redirect
    return redirect(url_for("admin_dashboard"))


@app.route(ADMIN_PREFIX)
@login_required
def admin_dashboard():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    counts = conn.execute(
        """SELECT s.slug, s.name, s.hindi, COUNT(n.id) AS cnt
           FROM subjects s LEFT JOIN notes n ON n.subject_slug = s.slug
           GROUP BY s.id ORDER BY s.id"""
    ).fetchall()
    total_notes = len(notes)
    total_files = 0
    for f in (PDF_FOLDER, HTML_FOLDER):
        total_files += len([x for x in os.listdir(f) if not x.startswith('.')])
    conn.close()
    # Subject-wise grouping: har subject ke notes serial mein (id order)
    by_subject = {}
    for n in notes:
        n = dict(n)
        by_subject.setdefault(n["subject_slug"], []).append(n)
    # subject slug ke saath name/emoji
    for s in dict(by_subject):
        subj = get_subject(s)
        if subj:
            by_subject[s].insert(0, {"__meta__": True, "name": subj["name"], "hindi": subj["hindi"], "slug": s})
    return render_template(
        "admin_dashboard.html",
        notes=[dict(n) for n in notes],
        counts=[dict(c) for c in counts],
        total_notes=total_notes,
        total_files=total_files,
        by_subject=by_subject,
        ADMIN_USERNAME=ADMIN_USERNAME,
    )


@app.route(ADMIN_PREFIX + "/upload", methods=["GET", "POST"])
@login_required
def admin_upload():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject_slug = request.form.get("subject_slug", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0")
        original_price = request.form.get("original_price", "") or None
        pages = request.form.get("pages", "") or None
        language = request.form.get("language", "Hindi + English").strip()
        featured = 1 if request.form.get("featured") else 0
        file = request.files.get("file")

        if not title or not subject_slug or not file or not file.filename:
            flash("Title, subject aur file sab zaroori hai.", "error")
            return redirect(url_for("admin_upload"))
        if not allowed_file(file.filename):
            flash("Sirf PDF (.pdf) ya HTML (.html/.htm) file upload kar sakte hain.", "error")
            return redirect(url_for("admin_upload"))
        if not get_subject(subject_slug):
            flash("Aisa subject exist nahi karta.", "error")
            return redirect(url_for("admin_upload"))

        try:
            price = float(price)
        except ValueError:
            price = 0
        try:
            original_price = float(original_price) if original_price else None
        except ValueError:
            original_price = None

        ext = get_ext(file.filename)
        original_name = secure_filename(file.filename)
        stored_name = f"{uuid.uuid4().hex}.{ext}"
        folder = PDF_FOLDER if ext == "pdf" else HTML_FOLDER
        rel_folder = "uploads/pdfs" if ext == "pdf" else "uploads/html"
        file_path = os.path.join(folder, stored_name)
        file.save(file_path)

        conn = get_db()
        conn.execute(
            """INSERT INTO notes
               (title, subject_slug, description, price, original_price,
                file_type, file_path, original_name, pages, language, featured, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, subject_slug, description, price, original_price,
             ext, os.path.join(rel_folder, stored_name), original_name,
             pages, language, featured, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        conn.close()
        flash(f"Note '{title}' upload ho gaya! ✅", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_upload.html", subjects=get_subjects())


@app.route(ADMIN_PREFIX + "/purchase", methods=["GET", "POST"])
@login_required
def admin_purchase():
    """UPI/manual payment confirm hone par user ko bundle access dene ke liye."""
    conn = get_db()
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        bundle_id = request.form.get("bundle_id", "")
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and bundle_id:
            exists = conn.execute("SELECT id FROM purchases WHERE user_id=? AND bundle_id=?",
                                  (user["id"], bundle_id)).fetchone()
            if not exists:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute("INSERT INTO purchases (user_id,bundle_id,email,created_at) VALUES (?,?,?,?)",
                             (user["id"], bundle_id, email, now))
                # M8: audit trail — kaunsa access kab manually diya
                conn.execute("INSERT INTO admin_actions (action, detail, created_at) VALUES (?,?,?)",
                             ("purchase_grant", f"bundle_id={bundle_id} user_id={user['id']} email={email}", now))
                conn.commit()
                flash(f"Purchase add ho gaya — {user['name']} ko bundle {bundle_id} ka access!", "success")
            else:
                flash("Ye purchase pehle se hai.", "info")
        else:
            flash("Email ya bundle galat hai.", "error")
    bundles = conn.execute("SELECT id,title,price FROM notes WHERE title LIKE '%Complete Bundle%' ORDER BY id").fetchall()
    conn.close()
    return render_template("admin_purchase.html", bundles=[dict(b) for b in bundles])


@app.route(ADMIN_PREFIX + "/note/<int:note_id>/delete", methods=["POST"])
@login_required
def admin_delete(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if row:
        # delete file from disk
        full = os.path.join(BASE_DIR, row["file_path"])
        if os.path.exists(full):
            try:
                os.remove(full)
            except OSError:
                pass
        conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        flash("Note delete ho gaya. 🗑️", "success")
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route(ADMIN_PREFIX + "/note/<int:note_id>/toggle", methods=["POST"])
@login_required
def admin_toggle(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if row:
        new_val = 0 if row["featured"] else 1
        conn.execute("UPDATE notes SET featured=? WHERE id=?", (new_val, note_id))
        conn.commit()
    conn.close()
    # NOTE: request.referrer par redirect nahi karte (referrer-controlled
    # redirect) — hamesha dashboard par wapas.
    return redirect(url_for("admin_dashboard"))


@app.route(ADMIN_PREFIX + "/subjects", methods=["GET", "POST"])
@login_required
def admin_subjects():
    if request.method == "POST":
        action = request.form.get("action")
        conn = get_db()
        if action == "add":
            name = request.form.get("name", "").strip()
            hindi = request.form.get("hindi", "").strip()
            slug = request.form.get("slug", "").strip() or slugify(name)
            if name and slug:
                try:
                    conn.execute(
                        "INSERT INTO subjects (slug, name, hindi) VALUES (?, ?, ?)",
                        (slug, name, hindi),
                    )
                    conn.commit()
                    flash(f"Subject '{name}' add ho gaya.", "success")
                except sqlite3.IntegrityError:
                    flash("Ye slug pehle se exist karta hai.", "error")
                invalidate_subjects_cache()
        elif action == "delete":
            sid = request.form.get("id")
            conn.execute("DELETE FROM subjects WHERE id=?", (sid,))
            conn.commit()
            flash("Subject delete ho gaya.", "info")
            invalidate_subjects_cache()
        conn.close()
        return redirect(url_for("admin_subjects"))
    return render_template("admin_subjects.html", subjects=get_subjects())


def slugify(text):
    import re
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "subject"


# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(413)
def too_large(e):
    return render_template("413.html"), 413


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print(f"  {SITE_NAME} chal raha hai!")
    print(f"  Storefront: http://127.0.0.1:5000")
    print(f"  Admin (secret): http://127.0.0.1:5000{ADMIN_PREFIX}/login")
    print("=" * 60)
    # NOTE: debug=False — debug=True production par Werkzeug debugger (RCE)
    # expose kar deta hai. Local development server hi hai ye.
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
