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

# ---- Aapki settings (change kar sakte hain) ----
SITE_NAME = "UPSC Notes Store"
SITE_TAGLINE = "Premium UPSC Notes — Ek Jagah, Sab Subjects"
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
# Password — environment variable se, warna default. Render par env variable set karein!
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "aj521900")
SESSION_SECRET = os.environ.get("SESSION_SECRET", "change-this-secret-key-please-123")

# UPI details for manual payment (buyer aapko contact karega)
UPI_ID = os.environ.get("UPI_ID", "9569431430@ybl")
UPI_QR_FILENAME = "qr.png"           # uploads/upi/qr.png mein rakhin
SELLER_PHONE = os.environ.get("SELLER_PHONE", "+91-9569431430")
SELLER_WHATSAPP = os.environ.get("SELLER_WHATSAPP", "+919569431430")
SELLER_EMAIL = os.environ.get("SELLER_EMAIL", "as5093220@gmail.com")

# Razorpay (Test Mode abhi)
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_TO7y62j31VXybk")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "8gywbRTay4qslNVywyLWEp4L")

ALLOWED_EXTENSIONS = {"pdf", "html", "htm"}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max file

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

# Reload fix: ensure fresh content on every load (no stale cache)
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
    return resp

for folder in (PDF_FOLDER, HTML_FOLDER, UPI_FOLDER):
    os.makedirs(folder, exist_ok=True)


# ============================================================
# DATABASE HELPERS
# ============================================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
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


def get_subjects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM subjects ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


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
    "prelims": "🎯", "mains": "✍️", "other": "📚",
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


DEMO_PREVIEW_IDS = _compute_demo_preview_ids()


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
        "demo_preview_ids": DEMO_PREVIEW_IDS,
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
    subject_counts = [dict(r) for r in subject_counts if r["slug"] not in child_slugs and r["slug"] != "geography-optional"]
    # har subject ka bundle (price + id) add karo — Buy button ke liye (conn close se PEHLE)
    for sc in subject_counts:
        b = conn.execute(
            "SELECT id, price, original_price FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%' LIMIT 1",
            (sc["slug"],)).fetchone()
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
            children.append(c)
    conn.close()
    return render_template("subject.html", subject=subj, notes=[dict(n) for n in rows], children=children)


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
    - Individual files → sirf demo/preview note khulta hai, baaki Buy page par redirect.
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
                    pf["content"] = base64.b64encode((get_note_content(pf) or "").encode("utf-8")).decode()
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
            first_row = conn.execute("SELECT * FROM notes WHERE id=?", (topics[0]["id"],)).fetchone()
            if first_row:
                raw = get_note_content(dict(first_row)) or ""
                first_content = base64.b64encode(raw.encode("utf-8")).decode()
        elif child_parts and child_parts[0]["preview_file"]:
            raw = get_note_content(child_parts[0]["preview_file"]) or ""
            first_content = base64.b64encode(raw.encode("utf-8")).decode()
        conn.close()
        return render_template("preview.html", bundle=note, topics=topics, first_content=first_content, purchased=purchased, child_parts=child_parts)
    # Individual → demo ids OR purchased subject ke notes khule
    has_access = session.get("is_admin") or note_id in DEMO_PREVIEW_IDS
    if not has_access and session.get("user_id"):
        # kya user ne is subject ka bundle kharida hai?
        bought = conn.execute(
            "SELECT id FROM purchases WHERE user_id=? AND bundle_id IN "
            "(SELECT id FROM notes WHERE subject_slug=? AND title LIKE '%Complete Bundle%')",
            (session["user_id"], note["subject_slug"])).fetchone()
        has_access = bool(bought)
    if not has_access:
        conn.close()
        return redirect(url_for("buy_note", note_id=note_id))
    content = get_note_content(note)
    conn.close()
    if note["file_type"] == "html" and content:
        return Response(clean_note_html(content), mimetype="text/html")
    full = os.path.join(BASE_DIR, note["file_path"])
    if not os.path.exists(full):
        abort(404)
    folder = os.path.dirname(full)
    name = os.path.basename(full)
    return send_from_directory(folder, name, as_attachment=False)


def bundle_preview_sample(content):
    """Bundle HTML se cover + pehla chapter dikhao, SAB CSS include karke
    (taaki chapter decorated dikhe, plain text nahi)."""
    import re
    # Sab <style> blocks extract karo (head + har chapter ke)
    styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.S)
    # clean each style: remove @import / @font-face file refs
    cleaned_styles = []
    for s in styles:
        s = re.sub(r"@import[^;]+;", "", s)
        s = re.sub(r"@font-face\s*\{[^}]*file:[^}]*\}", "", s, flags=re.S)
        cleaned_styles.append(s)
    all_css = "\n".join(cleaned_styles)

    # Cover section (bundle-cover, bina TOC)
    cover = ""
    m = re.search(r'<div class="bundle-cover">(.*?)(</div>\s*</div>|<div class="bundle-toc">)', content, re.S)
    if m:
        cover = '<div class="bundle-cover">' + m.group(1) + '</div></div>'

    # Pehla section (pehla bundle-section, agle section tak)
    sample = ""
    m1 = re.search(r'<div style="page-break-before:always;" class="bundle-section">', content)
    if m1:
        start = m1.start()
        m2 = re.search(r'<div style="page-break-before:always;" class="bundle-section">', content[start+10:])
        end = (start + 10 + m2.start()) if m2 else len(content)
        sample = content[start:end]

    notice = ('<div style="background:#fef3c7;border:1px solid #d97706;border-radius:10px;padding:14px 18px;'
              'margin:14px auto;max-width:820px;text-align:center;font-family:Arial,sans-serif;'
              'color:#7c2d12;font-size:14px;">'
              '👁️ <b>Ye sirf PREVIEW hai</b> — ek sample chapter dikhaya ja raha hai. '
              'Poora bundle kharidne ke liye <b>🛒 Buy</b> button dabayein.</div>')
    return (f'<!DOCTYPE html><html lang="hi"><head><meta charset="UTF-8"><title>Preview</title>'
            f'<style>{all_css}</style></head><body>{notice}{cover}{sample}</body></html>')


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
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
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
    """Razorpay order create karo (test mode)."""
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
    amount_paise = int(round(note["price"] * 100))
    try:
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"note_{note_id}",
            "payment_capture": 1,
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
    """Razorpay payment verify karo."""
    params = request.form.to_dict()
    client = _get_razorpay_client()
    note_id = request.form.get("note_id")
    if client is not None:
        try:
            client.utility.verify_payment_signature(params)
            payment_id = params.get("razorpay_payment_id")
            conn = get_db()
            # record payment
            conn.execute(
                "INSERT INTO payments (note_id, payment_id, order_id, amount, status, email, created_at) VALUES (?,?,?,?,?,?,?)",
                (note_id, payment_id, params.get("razorpay_order_id"), request.form.get("amount"), "paid", request.form.get("email", ""), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            # purchase record — user ko bundle access milta hai
            if session.get("user_id"):
                conn.execute(
                    "INSERT INTO purchases (user_id, bundle_id, email, created_at) VALUES (?,?,?,?)",
                    (session["user_id"], note_id, session.get("user_name",""), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                )
            conn.commit()
            conn.close()
            flash("Payment successful! ✅ Notes aapko WhatsApp par bheja jayega.", "success")
            return redirect(url_for("buy_success", note_id=note_id, payment_id=payment_id))
        except Exception as e:
            flash(f"Payment verify error: {e}", "error")
    return redirect(url_for("buy_note", note_id=int(note_id) if note_id else 1))


@app.route("/buy/success/<int:note_id>")
def buy_success(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    note = dict(row) if row else None
    return render_template("buy_success.html", note=note, payment_id=request.args.get("payment_id"))


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
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not name or not email or not password:
            flash("Naam, email aur password sab zaroori hai.", "error")
            return redirect(url_for("signup"))
        if password != confirm:
            flash("Password aur confirm password match nahi karte.", "error")
            return redirect(url_for("signup"))
        if len(password) < 4:
            flash("Password kam se kam 4 characters ka rakhein.", "error")
            return redirect(url_for("signup"))
        conn = get_db()
        exists = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if exists:
            conn.close()
            flash("Is email se account pehle se hai. Login karein.", "error")
            return redirect(url_for("login"))
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
        return redirect(url_for("user_dashboard"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}! 👋", "success")
            return redirect(url_for("user_dashboard"))
        flash("Galat email ya password!", "error")
    return render_template("login.html")


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
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    next_url = request.args.get("next") or url_for("admin_dashboard")
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Welcome back, Admin! 👋", "success")
            return redirect(next_url)
        flash("Galat username ya password! ❌", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Aap logout ho gaye hain.", "info")
    return redirect(url_for("index"))


@app.route("/admin")
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


@app.route("/admin/upload", methods=["GET", "POST"])
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


@app.route("/admin/note/<int:note_id>/delete", methods=["POST"])
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


@app.route("/admin/note/<int:note_id>/toggle", methods=["POST"])
@login_required
def admin_toggle(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if row:
        new_val = 0 if row["featured"] else 1
        conn.execute("UPDATE notes SET featured=? WHERE id=?", (new_val, note_id))
        conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("admin_dashboard"))


@app.route("/admin/subjects", methods=["GET", "POST"])
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
        elif action == "delete":
            sid = request.form.get("id")
            conn.execute("DELETE FROM subjects WHERE id=?", (sid,))
            conn.commit()
            flash("Subject delete ho gaya.", "info")
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
    print(f"  Admin URL:  http://127.0.0.1:5000/admin/login")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
