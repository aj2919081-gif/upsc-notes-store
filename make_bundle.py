import os, re, uuid, sqlite3, shutil
from datetime import datetime

SRC = "/home/user/uploads"
BASE = "/home/user/upsc-notes-store"
DB = os.path.join(BASE, "upsc.db")
HTML_DST = os.path.join(BASE, "uploads", "html")

# ordered file -> title
FILES = [
    ("c2.html",  "प्राचीन भारत का इतिहास - परिचय"),
    ("c3.html",  "पाषाण काल एवं 600 ई.पू. का परिवर्तन"),
    ("c4.html",  "पाषाण काल (भाग-2)"),
    ("c5.html",  "नवपाषाण काल एवं सिंधु घाटी सभ्यता"),
    ("c6.html",  "सिंधु घाटी सभ्यता"),
    ("c7.html",  "सिंधु घाटी सभ्यता - व्यापार एवं समाज"),
    ("c8.html",  "सिंधु घाटी + वैदिक सभ्यता"),
    ("c9.html",  "वैदिक सभ्यता"),
    ("c10.html", "वैदिक सभ्यता (भाग-04)"),
    ("c11.html", "वैदिक सभ्यता (भाग-05)"),
    ("c12.html", "ताम्र पाषाण काल एवं छठी शताब्दी ई.पू."),
    ("c13.html", "छठी शताब्दी ई.पू.: चीटशीट व मेन्स प्रश्न"),
    ("c14.html", "श्रमण धर्म"),
    ("c15.html", "बौद्ध एवं जैन धर्म"),
    ("c16.html", "बौद्ध और जैन धर्म (भाग-02)"),
    ("c17.html", "बौद्ध धर्म (भाग-03)"),
    ("c18.html", "जैन धर्म (भाग-04)"),
    ("c19.html", "जैन धर्म (भाग-05)"),
    ("c20.html", "मौर्य साम्राज्य"),
    ("c21.html", "मौर्य साम्राज्य (भाग-02)"),
    ("c22.html", "मौर्यवंश"),
    ("c23.html", "मौर्योत्तर काल (भाग-1)"),
    ("c24.html", "मौर्योत्तर काल (भाग-2)"),
    ("c25.html", "मौर्योत्तर काल (भाग-3)"),
    ("c26.html", "मौर्योत्तर काल (भाग-04) - समाज एवं संस्कृति"),
    ("c27.html", "मौर्योत्तरकालीन संस्कृति"),
    ("c28.html", "संगम संस्कृति (भाग-1)"),
    ("c29.html", "संगम संस्कृति (भाग-2)"),
    ("c32.html", "गुप्त साम्राज्य (भाग-03)"),
    ("c33.html", "गुप्त साम्राज्य (भाग-04) - प्रशासन"),
    ("c34.html", "गुप्त साम्राज्य (भाग-05) - अर्थव्यवस्था एवं समाज"),
    ("c35.html", "गुप्तकालीन संस्कृति एवं गुप्तोत्तर काल"),
]

def extract_body(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    return m.group(1) if m else html

def extract_styles(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    styles = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    # remove @font-face file:// references (fonts not available on server)
    cleaned = []
    for s in styles:
        s = re.sub(r"@font-face\s*\{[^}]*file:[^}]*\}", "", s, flags=re.S)
        s = re.sub(r"@import[^;]+;", "", s)
        cleaned.append(s)
    return "\n".join(cleaned)

merged_style = []
sections_html = []
toc_items = []

for idx, (fname, title) in enumerate(FILES, start=1):
    path = os.path.join(SRC, fname)
    if not os.path.exists(path):
        print("skip missing", fname)
        continue
    merged_style.append(extract_styles(path))
    body = extract_body(path)
    # add page break + section header
    sections_html.append(f'''
    <div style="page-break-before:always;" class="bundle-section">
      <div class="bundle-section-head">
        <span class="bundle-num">अध्याय {idx:02d}</span>
        <span class="bundle-title">{title}</span>
      </div>
      {body}
    </div>''')
    toc_items.append(f'<a href="#sec-{idx}"><span class="toc-num">{idx:02d}</span>{title}</a>')

# merge styles but scope conflicts by wrapping (best-effort)
merged_css = "\n".join(merged_style)

cover = f'''
<div class="bundle-cover">
  <div class="cover-badge">📜 Complete Bundle</div>
  <h1 class="cover-title">प्राचीन भारत का इतिहास</h1>
  <h2 class="cover-sub">सभी चीटशीट्स — एक साथ (32 अध्याय)</h2>
  <p class="cover-desc">पाषाण काल से गुप्तोत्तर काल तक — UPSC Prelims & Mains के लिए संपूर्ण एवं संकलित अध्ययन सामग्री।</p>
  <div class="cover-meta">📄 32 Cheatsheets &nbsp;·&nbsp; 🗣️ हिंदी &nbsp;·&nbsp; 🎯 UPSC / State PCS</div>
</div>
<div class="bundle-toc">
  <h3>📑 विषय-सूची (Table of Contents)</h3>
  <div class="toc-grid">{''.join(toc_items)}</div>
</div>
'''

final = f'''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<title>प्राचीन भारत का इतिहास - Complete Bundle (32 Cheatsheets)</title>
<style>
  @page {{ size: A4; margin: 10mm; }}
  body {{ font-family: 'Mangal','Nirmala UI','Arial Unicode MS','Noto Sans Devanagari',sans-serif; background:#f5f3ee; color:#1a1a1a; }}
  .bundle-cover {{ background: linear-gradient(135deg,#800020,#580014); color:#fff; border-radius:18px; padding:60px 40px; text-align:center; margin:20px auto; max-width:820px; }}
  .cover-badge {{ display:inline-block; background:#fff; color:#800020; font-weight:700; padding:6px 16px; border-radius:30px; letter-spacing:1px; font-size:14px; }}
  .cover-title {{ font-size:44px; margin:18px 0 6px; }}
  .cover-sub {{ font-size:24px; font-weight:400; opacity:.95; margin:0 0 16px; }}
  .cover-desc {{ font-size:16px; opacity:.9; max-width:560px; margin:0 auto 20px; line-height:1.6; }}
  .cover-meta {{ font-size:15px; opacity:.85; }}
  .bundle-toc {{ background:#fff; border-radius:18px; padding:30px; margin:24px auto; max-width:820px; box-shadow:0 4px 18px rgba(0,0,0,.08); }}
  .bundle-toc h3 {{ margin-top:0; color:#800020; }}
  .toc-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:8px 20px; }}
  .toc-grid a {{ display:flex; gap:10px; padding:7px 10px; border-radius:8px; background:#faf7f2; color:#333; text-decoration:none; font-size:14px; }}
  .toc-grid a:hover {{ background:#800020; color:#fff; }}
  .toc-num {{ color:#800020; font-weight:700; font-family:monospace; }}
  .bundle-section-head {{ display:flex; align-items:center; gap:12px; background:#800020; color:#fff; padding:12px 18px; border-radius:10px 10px 0 0; margin-top:20px; }}
  .bundle-num {{ background:#fff; color:#800020; font-weight:700; padding:2px 10px; border-radius:20px; font-size:13px; }}
  .bundle-title {{ font-size:18px; font-weight:700; }}
  .print-note {{ display:none; }}
</style>
{merged_css}
</head>
<body>
{cover}
{sections_html if isinstance(sections_html,str) else ''.join(sections_html)}
</body>
</html>'''

# save bundle
bundle_name = f"{uuid.uuid4().hex}.html"
bundle_rel = f"uploads/html/{bundle_name}"
bundle_path = os.path.join(HTML_DST, bundle_name)
with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(final)
print("Bundle HTML saved:", bundle_path, f"({os.path.getsize(bundle_path)//1024} KB)")

# insert into DB
PRICE = 499
ORIG_PRICE = 1499
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
conn = sqlite3.connect(DB)
conn.execute(
    """INSERT INTO notes (title, subject_slug, description, price, original_price, file_type,
        file_path, original_name, pages, language, featured, created_at)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
    ("प्राचीन भारत का इतिहास - Complete Bundle (सभी 32 चीटशीट्स)", "history",
     "पाषाण काल से गुप्तोत्तर काल तक की सभी 32 cheatsheets एक ही bundle में। UPSC Prelims & Mains के लिए संपूर्ण संकलित अध्ययन सामग्री — हिंदी में।",
     PRICE, ORIG_PRICE, "html", bundle_rel, "ancient-history-complete-bundle.html", 32,
     "हिंदी", 1, now),
)
conn.commit()
bundle_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()[0]
conn.close()
print("✅ Bundle note added! ID =", bundle_id, "| Price ₹", PRICE, "(orig ₹", ORIG_PRICE, ")")
print("   Featured = yes (homepage par dikhega)")
