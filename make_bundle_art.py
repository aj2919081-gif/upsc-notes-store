import os, re, uuid, sqlite3
from datetime import datetime

SRC = "/home/user/uploads"
BASE = "/home/user/upsc-notes-store"
DB = os.path.join(BASE, "upsc.db")
HTML_DST = os.path.join(BASE, "uploads", "html")

FILES = [
    ("c2.html",  "प्राचीन व मध्यकालीन भारतीय इतिहास के स्रोत"),
    ("c3.html",  "प्राचीन और मध्यकालीन इतिहास के स्रोत"),
    ("c4.html",  "प्राचीन व मध्यकालीन इतिहास के स्रोत (भाग-03)"),
    ("c5.html",  "भारतीय स्थापत्य कला"),
    ("c6.html",  "भारतीय स्थापत्य कला (भाग-02) - मौर्यकालीन"),
    ("c7.html",  "भारतीय स्थापत्य कला - व्याख्यान 07"),
    ("c8.html",  "भारतीय स्थापत्य कला"),
    ("c9.html",  "भारतीय चित्रकला और आधुनिक स्थापत्य कला"),
    ("c10.html", "भारतीय चित्रकला (भाग-02)"),
    ("c11.html", "बौद्ध और जैन धर्म का उदय"),
    ("c12.html", "बौद्ध और जैन धर्म के उदय"),
    ("c13.html", "बौद्ध और जैन धर्म का उदय व विकास (भाग 3)"),
    ("c14.html", "भक्ति और सूफी आंदोलन"),
    ("c15.html", "प्राचीन भारत में विज्ञान और प्रौद्योगिकी"),
    ("c16.html", "प्राचीन भारत में शिक्षा का विकास"),
    ("c17.html", "भारतीय शास्त्रीय नृत्य कला"),
    ("c18.html", "भारतीय संगीत कला"),
    ("c19.html", "भारतीय संगीत कला (भाग-02) + बाह्य संबंध"),
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
    cleaned = []
    for s in styles:
        s = re.sub(r"@font-face\s*\{[^}]*file:[^}]*\}", "", s, flags=re.S)
        s = re.sub(r"@import[^;]+;", "", s)
        cleaned.append(s)
    return "\n".join(cleaned)

merged_style, sections_html, toc_items = [], [], []
for idx, (fname, title) in enumerate(FILES, start=1):
    path = os.path.join(SRC, fname)
    if not os.path.exists(path):
        print("skip missing", fname); continue
    merged_style.append(extract_styles(path))
    body = extract_body(path)
    sections_html.append(f'''
    <div style="page-break-before:always;" class="bundle-section">
      <div class="bundle-section-head"><span class="bundle-num">अध्याय {idx:02d}</span><span class="bundle-title">{title}</span></div>
      {body}
    </div>''')
    toc_items.append(f'<a href="#sec-{idx}"><span class="toc-num">{idx:02d}</span>{title}</a>')

merged_css = "\n".join(merged_style)
cover = f'''
<div class="bundle-cover">
  <div class="cover-badge">🎨 Complete Bundle</div>
  <h1 class="cover-title">कला एवं संस्कृति</h1>
  <h2 class="cover-sub">Art & Culture — सभी चीटशीट्स एक साथ (18 अध्याय)</h2>
  <p class="cover-desc">इतिहास के स्रोत, स्थापत्य कला, चित्रकला, संगीत, नृत्य, भक्ति-सूफी आंदोलन, शिक्षा एवं विज्ञान — UPSC Prelims & Mains के लिए संपूर्ण अध्ययन सामग्री।</p>
  <div class="cover-meta">📄 18 Cheatsheets &nbsp;·&nbsp; 🗣️ हिंदी &nbsp;·&nbsp; 🎯 UPSC / State PCS</div>
</div>
<div class="bundle-toc"><h3>📑 विषय-सूची (Table of Contents)</h3><div class="toc-grid">{''.join(toc_items)}</div></div>
'''

final = f'''<!DOCTYPE html>
<html lang="hi"><head><meta charset="UTF-8">
<title>कला एवं संस्कृति - Complete Bundle (18 Cheatsheets)</title>
<style>
  @page {{ size: A4; margin: 10mm; }}
  body {{ font-family:'Mangal','Nirmala UI','Arial Unicode MS','Noto Sans Devanagari',sans-serif; background:#f6f4ef; color:#1a1a1a; }}
  .bundle-cover {{ background:linear-gradient(135deg,#854d0e,#451a03); color:#fff; border-radius:18px; padding:60px 40px; text-align:center; margin:20px auto; max-width:820px; }}
  .cover-badge {{ display:inline-block; background:#fff; color:#854d0e; font-weight:700; padding:6px 16px; border-radius:30px; letter-spacing:1px; font-size:14px; }}
  .cover-title {{ font-size:44px; margin:18px 0 6px; }}
  .cover-sub {{ font-size:24px; font-weight:400; opacity:.95; margin:0 0 16px; }}
  .cover-desc {{ font-size:16px; opacity:.9; max-width:560px; margin:0 auto 20px; line-height:1.6; }}
  .cover-meta {{ font-size:15px; opacity:.85; }}
  .bundle-toc {{ background:#fff; border-radius:18px; padding:30px; margin:24px auto; max-width:820px; box-shadow:0 4px 18px rgba(0,0,0,.08); }}
  .bundle-toc h3 {{ margin-top:0; color:#854d0e; }}
  .toc-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:8px 20px; }}
  .toc-grid a {{ display:flex; gap:10px; padding:7px 10px; border-radius:8px; background:#faf7f2; color:#333; text-decoration:none; font-size:14px; }}
  .toc-grid a:hover {{ background:#854d0e; color:#fff; }}
  .toc-num {{ color:#854d0e; font-weight:700; font-family:monospace; }}
  .bundle-section-head {{ display:flex; align-items:center; gap:12px; background:#854d0e; color:#fff; padding:12px 18px; border-radius:10px 10px 0 0; margin-top:20px; }}
  .bundle-num {{ background:#fff; color:#854d0e; font-weight:700; padding:2px 10px; border-radius:20px; font-size:13px; }}
  .bundle-title {{ font-size:18px; font-weight:700; }}
  .print-note {{ display:none; }}
</style>
{merged_css}
</head><body>
{cover}
{''.join(sections_html)}
</body></html>'''

bundle_name = f"{uuid.uuid4().hex}.html"
bundle_rel = f"uploads/html/{bundle_name}"
bundle_path = os.path.join(HTML_DST, bundle_name)
with open(bundle_path, "w", encoding="utf-8") as f:
    f.write(final)
print("Bundle HTML saved:", bundle_path, f"({os.path.getsize(bundle_path)//1024} KB)")

PRICE, ORIG_PRICE = 299, 899
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
conn = sqlite3.connect(DB)
conn.execute(
    """INSERT INTO notes (title, subject_slug, description, price, original_price, file_type,
        file_path, original_name, pages, language, featured, created_at)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
    ("कला एवं संस्कृति - Complete Bundle (सभी 18 चीटशीट्स)", "art-culture",
     "Art & Culture की सभी 18 cheatsheets एक bundle में — इतिहास के स्रोत, स्थापत्य कला, चित्रकला, संगीत, नृत्य, भक्ति-सूफी, शिक्षा एवं विज्ञान। UPSC Prelims & Mains हिंदी में।",
     PRICE, ORIG_PRICE, "html", bundle_rel, "art-culture-complete-bundle.html", 18,
     "हिंदी", 1, now),
)
conn.commit()
bundle_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()[0]
conn.close()
print("✅ Art & Culture Bundle added! ID =", bundle_id, "| Price ₹", PRICE, "(orig ₹", ORIG_PRICE, ")")
