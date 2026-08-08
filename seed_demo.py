import os, uuid, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "upsc.db")

samples = [
    ("Geography Complete Notes (Prelims + Mains)", "geography", "Complete geography notes covering Physical, Indian and World Geography. River systems, climate, geomorphology aur mapping ke saath.", 149, 299, 180),
    ("Indian Polity Master Notes", "polity", "Constitution, Preamble, Fundamental Rights, DPSP, Parliament, Judiciary — sab kuch crisp notes mein.", 129, 249, 150),
    ("Economics Basics for UPSC", "economics", "National Income, Inflation, Budget, Banking, Economic Survey highlights — simplified.", 139, 259, 160),
    ("Science & Technology Quick Notes", "science-tech", "Biotech, Space tech, Defence tech, AI, Nuclear — latest updates ke saath.", 119, 229, 120),
    ("Ancient & Medieval History", "history", "Harappa se Mughal tak — timeline, art, architecture aur society.", 129, 249, 170),
    ("Environment & Ecology Notes", "environment", "Ecology, Biodiversity, Climate change, National Parks & Protected areas.", 99, 199, 110),
]

html_body = """<!DOCTYPE html><html lang="hi"><head><meta charset="utf-8">
<title>{title}</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;max-width:760px;margin:30px auto;padding:0 20px;color:#222;line-height:1.7}}h1{{color:#1e4f8a}}h2{{color:#14365f;border-bottom:2px solid #e5e9f0;padding-bottom:6px}}li{{margin:6px 0}}</style>
</head><body>
<h1>{title}</h1>
<p><em>Ye ek sample note hai jo website ko demo ke liye dikhaya gaya hai. Aap ise admin panel se delete kar sakte hain aur apna real content upload kar sakte hain.</em></p>
<h2>Topic 1: Introduction</h2><p>{desc}</p>
<h2>Topic 2: Key Concepts</h2><ul><li>Concept A ki summary</li><li>Concept B ki summary</li><li>Important facts aur figures</li><li>PYQ (Previous Year Questions) analysis</li></ul>
<h2>Topic 3: Important Points</h2><p>Ye section exam point of view se most important points cover karta hai. Toppers ke notes se condensed.</p>
<h2>Conclusion</h2><p>Revision ke liye main points repeat karein. Sabhi UPSC prelims aur mains ke liye relevant.</p>
</body></html>"""

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
existing = conn.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
if existing > 0:
    print("Notes pehle se hain, seed skip.")
    conn.close()
    sys_exit = True
else:
    for i, (title, subj, desc, price, op, pages) in enumerate(samples):
        fname = f"{uuid.uuid4().hex}.html"
        fpath = os.path.join(BASE, "uploads", "html", fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html_body.format(title=title, desc=desc))
        conn.execute(
            "INSERT INTO notes (title, subject_slug, description, price, original_price, file_type, file_path, original_name, pages, language, featured, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (title, subj, desc, price, op, "html", f"uploads/html/{fname}", fname.replace('.html','.html'), pages, "Hindi + English", 1 if i < 3 else 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    conn.commit()
    print(f"✅ {len(samples)} sample notes add ho gaye.")
conn.close()
