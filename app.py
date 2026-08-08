"""UPSC Notes Store"""

import os
import sqlite3
import secrets
import uuid
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, session,
    send_from_directory, abort, flash, jsonify
)
from werkzeug.utils import secure_filename

from _embedded_templates import TEMPLATES as EMBEDDED_TEMPLATES

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
}


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
    recent = conn.execute(
        "SELECT * FROM notes ORDER BY created_at DESC LIMIT 9"
    ).fetchall()
    subject_counts = conn.execute(
        """SELECT s.slug, s.name, s.hindi, COUNT(n.id) AS cnt
           FROM subjects s LEFT JOIN notes n ON n.subject_slug = s.slug
           GROUP BY s.id ORDER BY s.id"""
    ).fetchall()
    conn.close()
    return render_template(
        "index.html",
        featured=[dict(n) for n in featured],
        recent=[dict(n) for n in recent],
        subject_counts=[dict(r) for r in subject_counts],
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


@app.route("/subject/<slug>")
def subject_page(slug):
    subj = get_subject(slug)
    if not subj:
        abort(404)
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM notes WHERE subject_slug=? ORDER BY created_at DESC",
        (slug,),
    ).fetchall()
    conn.close()
    return render_template("subject.html", subject=subj, notes=[dict(n) for n in rows])


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
    """Open the actual PDF/HTML note (download for pdf, inline for html)."""
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
    full = os.path.join(BASE_DIR, note["file_path"])
    if not os.path.exists(full):
        abort(404)
    folder = os.path.dirname(full)
    name = os.path.basename(full)
    if note["file_type"] == "pdf":
        return send_from_directory(folder, name, as_attachment=False)
    return send_from_directory(folder, name)


@app.route("/download/<int:note_id>")
def download_note(note_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not row:
        abort(404)
    note = dict(row)
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
    qr = None
    qr_path = os.path.join(UPI_FOLDER, UPI_QR_FILENAME)
    if os.path.exists(qr_path):
        qr = url_for("upi_qr", filename=UPI_QR_FILENAME)
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


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html",
                           SELLER_EMAIL=SELLER_EMAIL,
                           SELLER_WHATSAPP=SELLER_WHATSAPP)


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
    return render_template(
        "admin_dashboard.html",
        notes=[dict(n) for n in notes],
        counts=[dict(c) for c in counts],
        total_notes=total_notes,
        total_files=total_files,
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
