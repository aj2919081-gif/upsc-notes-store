"""Embedded templates - no separate templates/ folder needed."""

TEMPLATES = {
    '404.html': """{% extends "base.html" %}
{% block title %}404 — Not Found{% endblock %}
{% block content %}
<div class="notfound">
  <div class="big">404</div>
  <h2>Oops! Ye page nahi mila.</h2>
  <p style="color:var(--muted);">Jo page aap dhoond rahe hain woh exist nahi karta.</p>
  <a href="{{ url_for('index') }}" class="btn btn-primary">🏠 Home Chalein</a>
</div>
{% endblock %}
""",
    '413.html': """{% extends "base.html" %}
{% block title %}File too large{% endblock %}
{% block content %}
<div class="notfound">
  <div style="font-size:70px;">📦</div>
  <h2>File bahut bada hai!</h2>
  <p style="color:var(--muted);">Maximum file size 100 MB hai. Chhoti file try karein.</p>
  <a href="{{ url_for('admin_upload') }}" class="btn btn-primary">← Wapas Upload</a>
</div>
{% endblock %}
""",
    '_note_card.html': """<div class="note-card">
  <div class="note-thumb">
    {% if n.file_type == 'pdf' %}📄{% else %}🌐{% endif %}
    <span class="type-badge">{{ n.file_type }}</span>
    {% if n.featured %}<span class="badge-featured" style="position:absolute;left:10px;top:10px;">⭐ Featured</span>{% endif %}
  </div>
  <div class="note-body">
    <span class="subject-tag">{{ subject_emoji(n.subject_slug) }} {{ subject_name(n.subject_slug) }}</span>
    <h3><a href="{{ url_for('note_detail', note_id=n.id) }}">{{ n.title }}</a></h3>
    <p class="note-desc">{{ n.description[:120] }}{% if n.description|length > 120 %}...{% endif %}</p>
    <div class="price-row">
      <span class="price">₹{{ '%g' % n.price }}</span>
      {% if n.original_price and n.original_price > n.price %}<span class="orig-price">₹{{ '%g' % n.original_price }}</span>{% endif %}
    </div>
    <div class="note-actions">
      {% if n.id in demo_preview_ids or 'Complete Bundle' in (n.title or '') %}
        <a href="{{ url_for('note_view', note_id=n.id) }}" class="btn btn-ghost" target="_blank">👁️ Preview</a>
      {% endif %}
      <a href="{{ url_for('buy_note', note_id=n.id) }}" class="btn btn-primary">🛒 Buy</a>
    </div>
  </div>
</div>
""",
    'about.html': """{% extends "base.html" %}
{% block title %}About Us — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">

  <!-- Hero -->
  <div class="section-title">
    <div class="tag">About Us</div>
    <h2>UPSC Ki Taiyari, <em>Ek Jagah</em></h2>
    <p>{{ SITE_NAME }} ek premium platform hai jo UPSC, BPSC aur State PCS aspirants ke liye expert-curated notes provide karta hai.</p>
  </div>

  <!-- Mission / Vision -->
  <div class="detail-wrap">
    <div class="card">
      <h3 style="margin-top:0;">🎯 Hamara Mission</h3>
      <p>Har aspirant ko <b>high-quality, exam-focused notes</b> affordable price par provide karna. Hum samajhte hain ki sahi material hi success ki neev hai.</p>
    </div>
    <div class="card">
      <h3 style="margin-top:0;">🚀 Hamara Vision</h3>
      <p>UPSC ki taiyari ko <b>aasaan, structured aur effective</b> banana — taaki har student apne sapne poore kar sake, chaahe kahi bhi ho.</p>
    </div>
  </div>

  <!-- Stats -->
  <div class="stat-grid">
    <div class="stat"><div class="num">7+</div><div class="lbl">Complete Bundles</div></div>
    <div class="stat"><div class="num">365+</div><div class="lbl">Premium Notes</div></div>
    <div class="stat"><div class="num">15+</div><div class="lbl">Subjects Covered</div></div>
    <div class="stat"><div class="num">100%</div><div class="lbl">Hindi + English</div></div>
  </div>

  <!-- Features -->
  <div class="section-title">
    <div class="tag">Why Choose Us</div>
    <h2>Kyun Hum <em>Alag</em> Hain</h2>
  </div>
  <div class="feature-grid">
    <div class="feature-card"><div class="ico">📄</div><h3>Curated Notes</h3><p>Expert-curated cheatsheets Prelims + Mains ke liye</p></div>
    <div class="feature-card"><div class="ico">🗂️</div><h3>Subject-Wise</h3><p>Har subject alag — Geography, Polity, Economics, History &amp; more</p></div>
    <div class="feature-card"><div class="ico">🎯</div><h3>Exam-Focused</h3><p>PYQ aur trend analysis ke hisaab se taiyar</p></div>
    <div class="feature-card"><div class="ico">💳</div><h3>Simple Payment</h3><p>UPI / Razorpay se aasaan kharidari</p></div>
    <div class="feature-card"><div class="ico">⚡</div><h3>Instant Access</h3><p>Kharidte hi saari files chapter-wise open</p></div>
    <div class="feature-card"><div class="ico">🔐</div><h3>Secure Account</h3><p>Apne purchases hamesha apne account mein</p></div>
  </div>

  <!-- What we cover -->
  <div class="section-title">
    <div class="tag">Subjects</div>
    <h2>Hum Cover <em>Karte Hain</em></h2>
  </div>
  <div class="subject-grid">
    {% for s in all_subjects %}
      {% if s.name not in ['Geomorphology','Climatology','Oceanography','Indian Physiography','Mapping','Ancient History','Medieval History','Modern History','Post Independence','World History','Geography Optional'] %}
        <a class="subject-card" href="{{ url_for('subject_page', slug=s.slug) }}">
          <span class="emoji">{{ s.emoji }}</span>
          <span class="name">{{ s.name }}</span>
          <span class="count">{{ s.hindi }}</span>
        </a>
      {% endif %}
    {% endfor %}
  </div>

  <!-- CTA -->
  <div class="cta-banner">
    <h2>Taiyari Mein Aage Raho</h2>
    <p>Complete bundles mein saare notes ek saath — better price, better preparation.</p>
    <a href="{{ url_for('index') }}" class="btn btn-gold">📖 Notes Dekhein</a>
    <a href="{{ url_for('signup') }}" class="btn btn-line">✨ Account Banayein</a>
  </div>

</div>
{% endblock %}
""",
    'account.html': """{% extends "base.html" %}
{% block title %}My Account — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>🧑‍💼 My Account</h2>
    <p>Aapka profile.</p>
  </div>
  {% if user %}
  <div class="card" style="max-width:520px;">
    <div style="text-align:center; margin-bottom:20px;">
      <div style="width:80px;height:80px;border-radius:50%;background:var(--grad-emerald);color:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800;margin:0 auto;">{{ user.name[0]|upper }}</div>
    </div>
    <div class="list-keyval">
      <div><span>Naam</span><b>{{ user.name }}</b></div>
      <div><span>Email</span><b>{{ user.email }}</b></div>
      <div><span>Member Since</span><b>{{ user.created_at }}</b></div>
    </div>
    <div style="text-align:center; margin-top:16px;">
      <a href="{{ url_for('browse') }}" class="btn btn-gold">🛒 Notes Dekhein</a>
      <a href="{{ url_for('logout') }}" class="btn btn-danger" style="margin-left:8px;">Logout</a>
    </div>
  </div>
  {% else %}
  <div class="card" style="text-align:center; padding:40px;">
    <p>Account nahi mila. <a href="{{ url_for('login') }}">Login karein</a></p>
  </div>
  {% endif %}
</div>
{% endblock %}
""",
    'admin_dashboard.html': """{% extends "base.html" %}
{% block title %}Admin Dashboard — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>🧑‍💼 Admin Dashboard</h2>
    <p>Notes subject-wise — pehle subject chunein, phir files serial mein.</p>
  </div>

  <div class="stat-grid">
    <div class="stat"><div class="num">{{ total_notes }}</div><div class="lbl">Total Notes</div></div>
    <div class="stat"><div class="num">{{ counts|length }}</div><div class="lbl">Subjects</div></div>
  </div>

  <div class="toolbar">
    <a href="{{ url_for('admin_upload') }}" class="btn btn-primary">➕ Naya Note Upload</a>
    <a href="{{ url_for('admin_subjects') }}" class="btn btn-ghost">🗂️ Manage Subjects</a>
    <a href="{{ url_for('admin_purchase') }}" class="btn btn-gold">🎟️ User Ko Purchase Access</a>
  </div>

  <!-- Subjects ki list (clickable) -->
  <div class="section-title" style="margin-top:20px;">
    <div class="tag">Subjects</div>
    <h2>🗂️ Subject Chunein</h2>
    <p>Kisi bhi subject par click karein — neeche uski files serial mein dikhengi.</p>
  </div>
  <div class="subject-grid">
    {% for c in counts %}
      <a class="subject-card" href="#sub-{{ c.slug }}">
        <span class="emoji">{{ subject_emoji(c.slug) }}</span>
        <span class="name">{{ c.name }}</span>
        <span class="count">{{ c.hindi }} · {{ c.cnt }} files</span>
      </a>
    {% endfor %}
  </div>

  <!-- Subject-wise files -->
  {% for slug, items in by_subject.items() %}
    <div class="section-title" id="sub-{{ slug }}" style="margin-top:40px;">
      <div class="tag">Subject</div>
      <h2>{{ subject_emoji(slug) }} {{ subject_name(slug) }} <span style="font-size:16px;color:var(--muted);font-weight:400">({{ items|selectattr('__meta__','undefined')|list|length }} files)</span></h2>
    </div>
    <table class="admin-table">
      <thead>
        <tr><th>#</th><th>Title</th><th>Type</th><th style="width:180px;">Actions</th></tr>
      </thead>
      <tbody>
        {% set ns = namespace(c=0) %}
        {% for n in items %}
          {% if n.__meta__ is defined %}
          {% else %}
            {% set ns.c = ns.c + 1 %}
            <tr>
              <td>{{ ns.c }}</td>
              <td><b>{{ n.title }}</b></td>
              <td><span class="type-badge" style="position:static;background:var(--emerald);">{{ n.file_type }}</span></td>
              <td>
                <a href="{{ url_for('note_view', note_id=n.id) }}" class="btn btn-sm btn-ghost" target="_blank">👁️ Open</a>
                <a href="{{ url_for('download_note', note_id=n.id) }}" class="btn btn-sm btn-gold">⬇️ Free</a>
                <form method="post" action="{{ url_for('admin_delete', note_id=n.id) }}" style="display:inline;"
                      onsubmit="return confirm('Delete \\'{{ n.title }}\\'?');">
                  <button class="btn btn-sm btn-danger">🗑️</button>
                </form>
              </td>
            </tr>
          {% endif %}
        {% endfor %}
      </tbody>
    </table>
  {% endfor %}

</div>
{% endblock %}
""",
    'admin_login.html': """{% extends "base.html" %}
{% block title %}Admin Login — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="auth-wrap">
  <div class="card">
    <div style="text-align:center; margin-bottom:20px;">
      <div style="font-size:50px;">🔐</div>
      <h2 style="margin:8px 0 4px;">Admin Login</h2>
      <p style="color:var(--muted); margin:0; font-size:14px;">Notes upload/delete karne ke liye login karein.</p>
    </div>

    <form method="POST">
      <div class="form-group">
        <label>Username</label>
        <input type="text" name="username" required placeholder="admin" autocomplete="username">
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" name="password" required placeholder="••••••••" autocomplete="current-password">
      </div>
      <button type="submit" class="btn btn-primary" style="width:100%;">Login</button>
    </form>

    <p style="text-align:center; font-size:13px; color:var(--muted); margin-top:14px;">
      Username: <b>admin</b><br>(Password aapne set kiya hai — app.py mein change kar sakte hain)
    </p>
  </div>
</div>
{% endblock %}
""",
    'admin_purchase.html': """{% extends "base.html" %}
{% block title %}Add Purchase — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>🎟️ User Ko Purchase Access Denein</h2>
    <p>UPI/manual payment confirm hone par user ka email + bundle select karke access dein.</p>
  </div>

  <div class="card" style="max-width:560px;">
    <form method="POST">
      <div class="form-group">
        <label>User ka Email</label>
        <input type="email" name="email" required placeholder="customer@example.com">
      </div>
      <div class="form-group">
        <label>Bundle</label>
        <select name="bundle_id" required>
          {% for b in bundles %}
            <option value="{{ b.id }}">{{ b.title }} — ₹{{ '%g' % b.price }}</option>
          {% endfor %}
        </select>
      </div>
      <button type="submit" class="btn btn-primary">✅ Access Denein</button>
    </form>
  </div>

  <div style="margin-top:20px;">
    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-ghost">← Dashboard</a>
  </div>
</div>
{% endblock %}
""",
    'admin_subjects.html': """{% extends "base.html" %}
{% block title %}Manage Subjects — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="breadcrumb"><a href="{{ url_for('admin_dashboard') }}">← Dashboard</a></div>
  <div class="section-title">
    <h2>🗂️ Manage Subjects</h2>
    <p>Naya subject add karein ya purana delete karein.</p>
  </div>

  <div class="card" style="max-width:760px; margin-bottom:24px;">
    <h3 style="margin-top:0;">Naya Subject Add Karein</h3>
    <form method="POST">
      <input type="hidden" name="action" value="add">
      <div class="form-row">
        <div class="form-group">
          <label>Name *</label>
          <input type="text" name="name" required placeholder="e.g. Disaster Management">
        </div>
        <div class="form-group">
          <label>Hindi Name</label>
          <input type="text" name="hindi" placeholder="e.g. आपदा प्रबंधन">
        </div>
      </div>
      <div class="form-group">
        <label>Slug (URL) — khali chhodo, auto ban jayega</label>
        <input type="text" name="slug" placeholder="e.g. disaster-management">
      </div>
      <button class="btn btn-primary" type="submit">➕ Subject Add Karein</button>
    </form>
  </div>

  <h3>Subjects ({{ subjects|length }})</h3>
  <table class="admin-table">
    <thead><tr><th>Emoji</th><th>Name</th><th>Hindi</th><th>Slug</th><th style="width:100px;">Action</th></tr></thead>
    <tbody>
      {% for s in subjects %}
      <tr>
        <td>{{ subject_emoji(s.slug) }}</td>
        <td><b>{{ s.name }}</b></td>
        <td>{{ s.hindi }}</td>
        <td style="color:var(--muted);">{{ s.slug }}</td>
        <td>
          <form method="POST" onsubmit="return confirm('Subject \\'{{ s.name }}\\' delete karein?');">
            <input type="hidden" name="action" value="delete">
            <input type="hidden" name="id" value="{{ s.id }}">
            <button class="btn btn-sm btn-danger">🗑️</button>
          </form>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <p style="font-size:13px;color:var(--muted);">Note: kisi subject mein notes hon, to pehle woh notes delete karein tabhi subject delete hoga.</p>
</div>
{% endblock %}
""",
    'admin_upload.html': """{% extends "base.html" %}
{% block title %}Upload Note — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="breadcrumb"><a href="{{ url_for('admin_dashboard') }}">← Dashboard</a></div>
  <div class="section-title">
    <h2>➕ Naya Note Upload</h2>
    <p>PDF ya HTML file upload karein. Saari details bharein aur submit karein.</p>
  </div>

  <div class="card" style="max-width:760px;">
    <form method="POST" enctype="multipart/form-data">
      <div class="form-group">
        <label>Note ka Title *</label>
        <input type="text" name="title" required placeholder="e.g. Geography Complete Notes for Prelims">
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Subject *</label>
          <select name="subject_slug" required>
            {% for s in subjects %}
              <option value="{{ s.slug }}">{{ subject_emoji(s.slug) }} {{ s.name }} ({{ s.hindi }})</option>
            {% endfor %}
          </select>
        </div>
        <div class="form-group">
          <label>Language</label>
          <input type="text" name="language" value="Hindi + English" placeholder="Hindi, English, Hindi + English">
        </div>
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea name="description" rows="3" placeholder="Is note mein kya-kya covered hai..."></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Price (₹) *</label>
          <input type="number" name="price" step="0.01" min="0" required placeholder="99">
        </div>
        <div class="form-group">
          <label>Original Price (₹) — optional, discount dikhane ke liye</label>
          <input type="number" name="original_price" step="0.01" min="0" placeholder="199">
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Pages (optional)</label>
          <input type="number" name="pages" min="0" placeholder="150">
        </div>
        <div class="form-group">
          <label>File * (.pdf ya .html)</label>
          <input type="file" name="file" accept=".pdf,.html,.htm" required>
        </div>
      </div>

      <div class="form-group checkbox">
        <input type="checkbox" name="featured" value="1" id="feat">
        <label for="feat" style="margin:0;">⭐ Featured note banayein (homepage par dikhega)</label>
      </div>

      <div class="toolbar" style="margin-top:20px;">
        <button type="submit" class="btn btn-primary" style="font-size:16px;">📤 Upload Karin</button>
        <a href="{{ url_for('admin_dashboard') }}" class="btn btn-ghost">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}
""",
    'base.html': """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ SITE_NAME }}{% endblock %}</title>
  <meta name="description" content="{{ SITE_TAGLINE }}">
  <meta name="keywords" content="UPSC notes, UPSC study material, UPSC cheat sheets, IAS notes, geography notes UPSC, polity notes, economics notes, history notes, UPSC prelims, UPSC mains, BPSC notes, State PCS notes, free UPSC notes">
  <meta name="robots" content="index, follow">
  <meta name="author" content="{{ SITE_NAME }}">
  <meta property="og:title" content="{{ SITE_NAME }}">
  <meta property="og:description" content="{{ SITE_TAGLINE }}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary">
  <link rel="canonical" href="{{ request.url }}">
  <style>
  /* ============================================================
   UPSC Notes Store — PREMIUM EDITION
   Luxury feel: dark emerald + gold, refined typography,
   glassmorphism, smooth animations
   ============================================================ */
:root {
  --emerald: #6c2bd9;
  --emerald-dark: #4b1a9e;
  --emerald-deep: #2d0d66;
  --gold: #c9a227;
  --gold-light: #e6c25c;
  --cream: #f8f6fc;
  --white: #ffffff;
  --ink: #1a1130;
  --muted: #6b5f85;
  --line: rgba(108, 43, 217, 0.12);
  --shadow-sm: 0 2px 10px rgba(45, 13, 102, 0.06);
  --shadow: 0 10px 34px rgba(45, 13, 102, 0.12);
  --shadow-lg: 0 24px 60px rgba(45, 13, 102, 0.18);
  --radius: 20px;
  --radius-sm: 12px;
  --grad-gold: linear-gradient(120deg, #b388ff, #d9c2ff, #c9a227);
  --grad-emerald: linear-gradient(135deg, #6c2bd9, #4b1a9e, #2d0d66);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
html, body { margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', -apple-system, 'Georgia', 'Roboto', system-ui, sans-serif;
  color: var(--ink); line-height: 1.65;
  background-color: var(--cream);
}
a { color: var(--emerald); text-decoration: none; }
a:hover { text-decoration: none; }
.container { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
img { max-width: 100%; }

/* ===== Elegant top ribbon ===== */
.topbar {
  background: linear-gradient(90deg, var(--emerald-deep), var(--emerald), var(--emerald-deep));
  color: rgba(255,255,255,.85); font-size: 12.5px; letter-spacing: .4px; padding: 7px 0;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.topbar .container { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px; }
.topbar a { color: var(--gold-light); font-weight: 600; }

/* ===== Glass header ===== */
header.site {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,.78);
  backdrop-filter: blur(18px) saturate(160%);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  border-bottom: 1px solid var(--line);
}
.navbar { display: flex; align-items: center; justify-content: space-between; height: 74px; gap: 18px; }
.brand { display: flex; align-items: center; gap: 13px; }
.brand-logo {
  width: 48px; height: 48px; border-radius: 15px; display: grid; place-items: center;
  background: var(--grad-emerald); color: #fff; font-weight: 800; font-size: 22px;
  box-shadow: 0 6px 18px rgba(45,13,102,.3);
  position: relative; overflow: hidden;
}
.brand-logo::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(255,255,255,.25), transparent 60%);
}
.brand-name { font-size: 21px; font-weight: 800; color: var(--ink); letter-spacing: -0.4px; }
.brand-name span { background: var(--grad-gold); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.brand-tag { font-size: 11px; color: var(--muted); letter-spacing: .5px; text-transform: uppercase; }

.nav-links { display: flex; align-items: center; gap: 4px; }
.nav-links a {
  padding: 9px 15px; border-radius: 11px; color: var(--ink); font-weight: 600; font-size: 15px;
  transition: .18s; position: relative;
  /* Neon glow — saare buttons glow karein */
  box-shadow: 0 0 8px rgba(108,43,217,.15), 0 0 16px rgba(108,43,217,.08);
  border: 1px solid rgba(108,43,217,.15);
}
.nav-links a:hover {
  background: rgba(108,43,217,.12); color: var(--emerald);
  box-shadow: 0 0 14px rgba(108,43,217,.4), 0 0 30px rgba(108,43,217,.2);
  transform: translateY(-1px);
}
.nav-links a.admin-btn {
  background: var(--grad-emerald); color: #fff; font-weight: 700; margin-left: 4px;
  box-shadow: 0 4px 14px rgba(45,13,102,.25), 0 0 10px rgba(108,43,217,.3);
}
.nav-links a.admin-btn:hover { transform: translateY(-1px); color: #fff; box-shadow: 0 0 18px rgba(108,43,217,.6), 0 0 40px rgba(108,43,217,.3); }

.searchbar { display: flex; flex: 1; max-width: 320px; }
.searchbar input {
  flex: 1; padding: 11px 15px; border: 1px solid var(--line); border-radius: 12px 0 0 12px;
  font-size: 14px; outline: none; background: rgba(255,255,255,.7);
}
.searchbar input:focus { border-color: var(--gold); box-shadow: 0 0 0 3px rgba(201,162,39,.15); }
.searchbar button {
  padding: 0 18px; border: none; background: var(--emerald); color: #fff;
  border-radius: 0 12px 12px 0; cursor: pointer; font-size: 15px; transition: .18s;
}
.searchbar button:hover { background: var(--emerald-dark); }

.theme-toggle {
  background: rgba(108,43,217,.08); border: 1px solid var(--line); border-radius: 11px;
  padding: 10px 13px; cursor: pointer; font-size: 17px; line-height: 1; transition: .18s;
}
.theme-toggle:hover { border-color: var(--gold); }

/* ===== Hero — luxurious ===== */
.hero {
  position: relative; overflow: hidden; text-align: center; color: #fff;
  background: var(--grad-emerald);
  padding: 96px 0 110px;
}
.hero::before {
  content: ''; position: absolute; inset: 0;
  background:
    radial-gradient(circle at 12% 15%, rgba(201,162,39,.22), transparent 42%),
    radial-gradient(circle at 88% 80%, rgba(255,255,255,.10), transparent 45%),
    repeating-linear-gradient(45deg, transparent 0 40px, rgba(255,255,255,.02) 40px 42px);
}
.hero::after {
  content: ''; position: absolute; left: 50%; bottom: -2px; transform: translateX(-50%);
  width: 240px; height: 4px; border-radius: 4px; background: var(--grad-gold);
}
.hero .container { position: relative; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 9px;
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
  padding: 9px 22px; border-radius: 40px; font-size: 13.5px; font-weight: 600; letter-spacing: .6px;
  backdrop-filter: blur(6px);
}
.hero h1 { font-size: 56px; margin: 26px 0 16px; font-weight: 800; letter-spacing: -1.2px; line-height: 1.08; }
.hero h1 .grad-text { background: var(--grad-gold); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 18px rgba(246,210,80,.55), 0 0 42px rgba(246,183,60,.35); }
.hero h1 { text-shadow: 0 0 20px rgba(120,220,170,.35), 0 0 60px rgba(108,43,217,.45); }
.hero p { font-size: 19px; opacity: .9; max-width: 650px; margin: 0 auto 34px; font-weight: 300; }
.hero .cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }

.btn {
  display: inline-block; padding: 14px 30px; border-radius: 13px; font-weight: 700; font-size: 15px;
  border: none; cursor: pointer; transition: .2s; text-decoration: none !important; letter-spacing: .3px;
}
.btn-gold { background: var(--grad-gold); color: #2a1d00; box-shadow: 0 8px 26px rgba(201,162,39,.4); }
.btn-gold:hover { transform: translateY(-2px); box-shadow: 0 0 18px rgba(246,210,80,.7), 0 0 45px rgba(246,183,60,.5), 0 12px 32px rgba(201,162,39,.5); }
.btn-line { background: rgba(255,255,255,.12); border: 1.5px solid rgba(255,255,255,.55); color: #fff; }
.btn-line:hover { background: rgba(255,255,255,.22); }
.btn-green { background: var(--emerald); color: #fff; }
.btn-green:hover { background: var(--emerald-dark); transform: translateY(-2px); }
.btn-sm { padding: 9px 16px; font-size: 13px; border-radius: 10px; }
.btn-ghost { background: rgba(108,43,217,.07); color: var(--emerald); }
.btn-ghost:hover { background: rgba(108,43,217,.13); }
.btn-danger { background: #dc2626; color: #fff; }

/* Hero stats */
.hero-stats { display: flex; gap: 56px; justify-content: center; margin-top: 52px; flex-wrap: wrap; }
.hero-stat { text-align: center; position: relative; }
.hero-stat:not(:last-child)::after {
  content: ''; position: absolute; right: -28px; top: 50%; transform: translateY(-50%);
  width: 1px; height: 44px; background: rgba(255,255,255,.2);
}
.hero-stat .num { font-size: 42px; font-weight: 800; background: var(--grad-gold); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.hero-stat .lbl { font-size: 13px; opacity: .8; letter-spacing: 1px; text-transform: uppercase; }

/* ===== Section titles ===== */
.section-title { margin: 60px 0 26px; text-align: center; }
.section-title .tag {
  display: inline-block; font-size: 12px; font-weight: 700; color: var(--gold); text-transform: uppercase;
  letter-spacing: 2.5px; margin-bottom: 8px;
}
.section-title h2 { font-size: 34px; margin: 4px 0 6px; font-weight: 800; letter-spacing: -0.6px; color: var(--ink); text-shadow: 0 0 14px rgba(108,43,217,.12); }
.section-title h2 em { font-style: normal; color: var(--emerald); text-shadow: 0 0 16px rgba(108,43,217,.35); }
.section-title p { color: var(--muted); margin: 0; }

/* ===== Subject cards — premium ===== */
.subject-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(165px, 1fr)); gap: 18px; }
.subject-card {
  background: var(--white); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 28px 14px; text-align: center; transition: .22s; display: block;
  box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
}
.subject-card::before {
  content: ''; position: absolute; inset: 0; opacity: 0; transition: .3s;
  background: linear-gradient(160deg, rgba(108,43,217,.06), transparent 60%);
  pointer-events: none; z-index: 1;
}
.subject-card > a { position: relative; z-index: 2; }
.subject-card > .btn { position: relative; z-index: 3; }
.subject-card:hover { transform: translateY(-6px); box-shadow: 0 0 22px rgba(108,43,217,.35), 0 0 50px rgba(108,43,217,.15), var(--shadow); border-color: rgba(201,162,39,.6); }
.subject-card:hover::before { opacity: 1; }
.subject-card .emoji { font-size: 38px; display: block; margin-bottom: 10px; filter: drop-shadow(0 3px 6px rgba(0,0,0,.1)); }
.subject-card .name { font-weight: 700; color: var(--ink); font-size: 15px; position: relative; }
.subject-card .count { font-size: 12px; color: var(--muted); margin-top: 4px; position: relative; }
.subject-card .exam-tag {
  display: inline-block; margin-top: 8px; padding: 4px 12px; border-radius: 20px;
  font-size: 11px; font-weight: 700; color: #fff; letter-spacing: .4px;
  background: linear-gradient(90deg, var(--emerald), var(--emerald-dark));
  box-shadow: 0 0 10px rgba(108,43,217,.3);
  position: relative;
}

/* ===== Note cards — luxury ===== */
.note-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(285px, 1fr)); gap: 26px; }
.note-card {
  background: var(--white); border: 1px solid var(--line); border-radius: var(--radius);
  overflow: hidden; display: flex; flex-direction: column; transition: .25s;
  box-shadow: var(--shadow-sm); position: relative;
}
.note-card:hover { transform: translateY(-8px); box-shadow: 0 0 26px rgba(108,43,217,.4), 0 0 60px rgba(108,43,217,.16), var(--shadow-lg); border-color: rgba(201,162,39,.55); }
.note-thumb {
  height: 150px; display: flex; align-items: center; justify-content: center; position: relative;
  background: linear-gradient(135deg, #efe9fc, #ddd0f5); font-size: 54px;
}
.note-thumb .type-badge {
  position: absolute; top: 12px; right: 12px; background: rgba(108,43,217,.88); color: #fff;
  font-size: 10px; font-weight: 700; padding: 4px 11px; border-radius: 20px; text-transform: uppercase; letter-spacing: .6px;
}
.badge-featured {
  display: inline-block; background: var(--grad-gold); color: #2a1d00; font-size: 11px; font-weight: 800;
  padding: 4px 11px; border-radius: 20px; position: absolute; left: 12px; top: 12px; box-shadow: 0 3px 10px rgba(0,0,0,.15);
}
.note-body { padding: 20px; display: flex; flex-direction: column; flex: 1; }
.note-body .subject-tag { font-size: 11.5px; color: var(--gold); font-weight: 700; text-transform: uppercase; letter-spacing: .8px; }
.note-body h3 { margin: 7px 0 9px; font-size: 18px; line-height: 1.35; }
.note-body h3 a { color: var(--ink); transition: .15s; }
.note-body h3 a:hover { color: var(--emerald); }
.note-desc { color: var(--muted); font-size: 14px; flex: 1; }
.price-row { display: flex; align-items: baseline; gap: 9px; margin-top: 13px; }
.price { font-size: 25px; font-weight: 800; color: var(--ink); }
.price.free { color: var(--emerald); }
.orig-price { color: var(--muted); text-decoration: line-through; font-size: 14px; }
.note-actions { display: flex; gap: 9px; margin-top: 15px; }
.note-actions .btn { flex: 1; text-align: center; font-size: 14px; padding: 11px; }

/* ===== Feature cards ===== */
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 20px; margin: 48px 0; }
.feature-card {
  background: var(--white); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 30px 22px; text-align: center; box-shadow: var(--shadow-sm); transition: .22s;
}
.feature-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.feature-card .ico {
  width: 62px; height: 62px; margin: 0 auto 16px; border-radius: 18px; display: grid; place-items: center;
  font-size: 28px; background: linear-gradient(135deg, #efe9fc, #ddd0f5);
  box-shadow: inset 0 0 0 1px rgba(108,43,217,.08);
}
.feature-card h3 { margin: 0 0 5px; font-size: 17px; }
.feature-card p { color: var(--muted); font-size: 13.5px; margin: 0; }

/* ===== CTA banner ===== */
.cta-banner {
  background: var(--grad-emerald); color: #fff; border-radius: var(--radius);
  padding: 54px 40px; text-align: center; margin: 60px 0; position: relative; overflow: hidden;
}
.cta-banner::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 20% 30%, rgba(201,162,39,.2), transparent 45%);
}
.cta-banner::after {
  content: ''; position: absolute; left: 50%; top: -1px; transform: translateX(-50%);
  width: 300px; height: 4px; border-radius: 4px; background: var(--grad-gold);
}
.cta-banner h2 { font-size: 32px; margin: 0 0 10px; position: relative; text-shadow: 0 0 20px rgba(246,210,80,.5), 0 0 50px rgba(246,183,60,.3); }

/* ===== UPSC OPTIONAL SECTION ===== */
.optional-section { margin: 40px 0; }
.optional-toggle {
  width: 100%; text-align: center; cursor: pointer; border: none; outline: none;
  background: var(--grad-emerald); color: #fff; border-radius: var(--radius);
  padding: 30px 20px; font-size: 22px; font-weight: 800; letter-spacing: .5px;
  box-shadow: 0 0 26px rgba(108,43,217,.35), 0 8px 30px rgba(45,13,102,.2);
  transition: .25s; position: relative; overflow: hidden; font-family: inherit;
}
.optional-toggle::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 50% 0%, rgba(246,210,80,.28), transparent 55%);
}
.optional-toggle:hover { transform: translateY(-2px); box-shadow: 0 0 40px rgba(246,210,80,.4), 0 0 80px rgba(108,43,217,.3); }
.optional-toggle .opt-emoji { font-size: 34px; display: block; margin-bottom: 8px; position: relative; }
.optional-toggle span { position: relative; }
.optional-toggle .opt-hint { display: block; font-size: 13px; font-weight: 500; opacity: .85; margin-top: 8px; position: relative; }
.optional-panel {
  background: var(--white); border: 1px solid var(--line); border-radius: var(--radius);
  margin-top: 16px; padding: 26px; box-shadow: var(--shadow); display: none;
}
.optional-panel.open { display: block; animation: optFade .35s ease; }
@keyframes optFade { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }
.optional-panel h3 { margin: 0 0 16px; font-size: 20px; }
.optional-panel h3 em { font-style: normal; color: var(--emerald); text-shadow: 0 0 14px rgba(108,43,217,.3); }
.optional-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 14px; }
.optional-card {
  background: var(--cream); border: 1px solid var(--line); border-radius: var(--radius-sm);
  padding: 22px 14px; text-align: center; transition: .2s; display: block;
  box-shadow: var(--shadow-sm);
}
.optional-card:hover { transform: translateY(-4px); border-color: var(--gold); box-shadow: 0 0 20px rgba(108,43,217,.25); }
.optional-card .emoji { font-size: 32px; display: block; margin-bottom: 8px; }
.optional-card .name { font-weight: 700; color: var(--ink); font-size: 15px; }
.optional-card .tag { font-size: 11px; color: var(--gold); font-weight: 700; text-transform: uppercase; letter-spacing: .5px; }
.optional-card.featured {
  border: 2px solid #b388ff; box-shadow: 0 0 28px rgba(108,43,217,.45), 0 0 60px rgba(108,43,217,.2);
  background: linear-gradient(135deg, #6c2bd9, #4b1a9e); color: #fff;
}
.optional-card.featured .name { color: #fff; font-size: 17px; font-weight: 800; }
.optional-card.featured .tag { color: #e6c25c; }
.optional-card.featured .emoji { filter: drop-shadow(0 2px 6px rgba(0,0,0,.3)); }

/* ===== NEON QUOTE SECTION ===== */
.quote-section { margin: 60px 0; text-align: center; }
.quote-box {
  background: var(--grad-emerald); border-radius: var(--radius); padding: 50px 36px;
  position: relative; overflow: hidden; border: 1px solid rgba(201,162,39,.4);
  box-shadow: 0 0 40px rgba(108,43,217,.4), 0 0 80px rgba(108,43,217,.2), var(--shadow-lg);
}
.quote-box::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 50% 0%, rgba(246,210,80,.25), transparent 55%);
}
.quote-mark {
  font-size: 80px; line-height: 1; color: var(--gold-light); font-family: Georgia, serif;
  text-shadow: 0 0 24px rgba(246,210,80,.7), 0 0 60px rgba(246,183,60,.4);
}
.quote-text {
  font-size: 26px; font-weight: 700; color: #fff; max-width: 720px; margin: 14px auto 10px;
  font-family: Georgia, 'Segoe UI', serif; font-style: italic; line-height: 1.5;
  text-shadow: 0 0 18px rgba(255,255,255,.4), 0 0 40px rgba(246,210,80,.35);
  transition: opacity .4s ease;
}
.quote-author {
  font-size: 14px; color: var(--gold-light); letter-spacing: 2px; text-transform: uppercase; font-weight: 700;
  text-shadow: 0 0 14px rgba(246,210,80,.6);
  transition: opacity .4s ease;
}
.cta-banner p { opacity: .9; max-width: 540px; margin: 0 auto 26px; position: relative; font-weight: 300; }

/* ===== TRUST / MINDSET SECTION ===== */
.trust-section { margin: 56px 0; text-align: center; }
.trust-badge {
  display: inline-flex; align-items: center; gap: 10px;
  background: linear-gradient(90deg, var(--emerald), var(--emerald-dark));
  color: #fff; padding: 12px 26px; border-radius: 40px; font-weight: 800; font-size: 20px;
  box-shadow: 0 0 24px rgba(108,43,217,.4), 0 0 60px rgba(108,43,217,.15);
}
.trust-badge .tnum { font-size: 28px; }
.trust-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 20px; margin: 34px 0; }
.trust-card {
  background: var(--white); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 30px 18px; box-shadow: var(--shadow-sm); transition: .2s;
}
.trust-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); border-color: rgba(201,162,39,.5); }
.trust-card .ico { font-size: 40px; margin-bottom: 10px; }
.trust-card .num { font-size: 34px; font-weight: 800; color: var(--emerald); }
.trust-card .lbl { color: var(--muted); font-size: 15px; margin-top: 4px; }
.trust-quote {
  background: var(--grad-emerald); border-radius: var(--radius); padding: 34px 28px;
  color: #fff; position: relative; overflow: hidden; margin-top: 24px;
}
.trust-quote::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 20% 20%, rgba(246,210,80,.2), transparent 50%); }
.trust-quote p { font-size: 22px; font-weight: 700; font-style: italic; position: relative; margin: 0 auto 10px; max-width: 720px; }
.trust-quote .by { font-size: 14px; color: var(--gold-light); position: relative; letter-spacing: 1px; }

/* ===== Cards ===== */
.card { background: var(--white); border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; box-shadow: var(--shadow-sm); }

/* ===== Flashes ===== */
.flashes { margin: 18px auto; max-width: 1180px; padding: 0 24px; }
.flash { padding: 14px 18px; border-radius: 12px; margin-bottom: 12px; font-weight: 600; }
.flash.success { background: #e6f7ed; color: #14532d; border: 1px solid #bbe7cc; }
.flash.error { background: #fee2e2; color: #7f1d1d; border: 1px solid #fecaca; }
.flash.info { background: #e0f2fe; color: #0c4a6e; border: 1px solid #bae6fd; }

/* ===== Forms ===== */
.form-group { margin-bottom: 17px; }
.form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 14px; }
.form-group input, .form-group textarea, .form-group select {
  width: 100%; padding: 12px 15px; border: 1px solid var(--line); border-radius: 11px; font-size: 15px;
  font-family: inherit; background: var(--white); transition: .15s;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
  outline: none; border-color: var(--gold); box-shadow: 0 0 0 3px rgba(201,162,39,.15);
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.checkbox { display: flex; align-items: center; gap: 8px; }
.checkbox input { width: auto; }
.toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 20px 0; }
.filter-bar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 22px; }
.filter-bar input, .filter-bar select { padding: 11px 14px; border: 1px solid var(--line); border-radius: 10px; font-size: 14px; background: var(--white); }

/* ===== Detail page ===== */
.detail-wrap { display: grid; grid-template-columns: 1fr 340px; gap: 32px; margin: 32px 0; }
.buy-box { position: sticky; top: 90px; }
.detail-title { font-size: 32px; margin: 12px 0; letter-spacing: -0.5px; }
.breadcrumb { font-size: 14px; color: var(--muted); margin: 20px 0 8px; }
.list-keyval { margin: 14px 0; }
.list-keyval div { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 14px; }
.list-keyval b { color: var(--ink); }

/* ===== Admin ===== */
.admin-table { width: 100%; border-collapse: collapse; background: var(--white); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-sm); }
.admin-table th, .admin-table td { padding: 13px 15px; text-align: left; border-bottom: 1px solid var(--line); font-size: 14px; vertical-align: middle; }
.admin-table th { background: linear-gradient(135deg, #f0f6f2, #e8f0eb); color: var(--emerald-dark); font-weight: 700; text-transform: uppercase; font-size: 12px; letter-spacing: .5px; }
.admin-table tr:hover td { background: #fafcfb; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 18px; margin: 22px 0; }
.stat { background: var(--white); border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; text-align: center; box-shadow: var(--shadow-sm); }
.stat .num { font-size: 38px; font-weight: 800; color: var(--emerald); }
.stat .lbl { color: var(--muted); font-size: 14px; }
.btn-warn { background: #fef3c7; color: #92400e; }
.auth-wrap { max-width: 440px; margin: 60px auto; }

/* ===== Footer ===== */
footer.site { background: var(--emerald-deep); color: rgba(255,255,255,.7); margin-top: 70px; padding: 56px 0 24px; position: relative; }
footer.site::before { content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 340px; height: 3px; background: var(--grad-gold); }
.footer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px,1fr)); gap: 30px; margin-bottom: 26px; }
footer h4 { color: #fff; margin: 0 0 14px; font-size: 16px; letter-spacing: .3px; }
footer a { color: rgba(255,255,255,.7); display: block; margin: 6px 0; font-size: 14px; transition: .15s; }
footer a:hover { color: var(--gold-light); }
footer .copy { border-top: 1px solid rgba(255,255,255,.1); padding-top: 18px; font-size: 13px; text-align: center; color: rgba(255,255,255,.45); }

/* ===== 404 ===== */
.notfound { text-align: center; padding: 90px 20px; }
.notfound .big { font-size: 100px; font-weight: 800; background: var(--grad-gold); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.notfound h2 { margin: 10px 0; }

/* ===== DARK MODE ===== */
body.dark-mode {
  --cream: #100b1a; --white: #1a1130; --ink: #ece6f7; --muted: #a89bc4; --line: rgba(255,255,255,.08);
  --shadow-sm: 0 2px 10px rgba(0,0,0,.4); --shadow: 0 10px 34px rgba(0,0,0,.5); --shadow-lg: 0 24px 60px rgba(0,0,0,.6);
}
body.dark-mode header.site { background: rgba(16,11,26,.85); }
body.dark-mode .brand-name { color: #fff; }
body.dark-mode .hero { background: var(--grad-emerald); }
body.dark-mode .topbar, body.dark-mode footer.site { background: #07030f; }
body.dark-mode .subject-card, body.dark-mode .note-card, body.dark-mode .feature-card, body.dark-mode .card, body.dark-mode .stat { background: var(--white); }
body.dark-mode .searchbar input, body.dark-mode .filter-bar input, body.dark-mode .filter-bar select,
body.dark-mode .form-group input, body.dark-mode .form-group textarea, body.dark-mode .form-group select { background: #120a22; color: #ece6f7; border-color: var(--line); }
body.dark-mode .note-thumb { background: linear-gradient(135deg, #2a1650, #1a0d33); }
body.dark-mode .nav-links a:hover, body.dark-mode .theme-toggle, body.dark-mode .btn-ghost { background: #251545; color: #ece6f7; box-shadow: 0 0 12px rgba(108,43,217,.3); }
body.dark-mode .admin-table { background: var(--white); }
body.dark-mode .admin-table th { background: #122019; color: #cfe7da; }

/* ===== Responsive ===== */
@media (max-width: 860px) {
  .navbar { flex-wrap: wrap; height: auto; padding: 14px 0; gap: 10px; }
  .searchbar { order: 3; max-width: 100%; width: 100%; }
  .hero h1 { font-size: 38px; }
  .hero-stats { gap: 30px; }
  .hero-stat:not(:last-child)::after { display: none; }
  .detail-wrap { grid-template-columns: 1fr; }
  .buy-box { position: static; }
  .form-row { grid-template-columns: 1fr; }
  .admin-table { display: block; overflow-x: auto; }
  .nav-links { flex-wrap: wrap; }
}

  </style>
</head>
<body>

  <div class="topbar">
    <div class="container">
      <span>&#10022; UPSC | BPSC | State PCS &#8212; Premium Notes</span>
      <span>{% if is_admin %}<a href="{{ url_for('admin_dashboard') }}">&#129489;&#8205;&#128187; Admin Panel</a>{% else %}<a href="{{ url_for('admin_login') }}">Admin Login</a>{% endif %}</span>
    </div>
  </div>

  <header class="site">
    <div class="container navbar">
      <a href="{{ url_for('index') }}" class="brand">
        <img src="{{ url_for('static', filename='aw-logo.png') }}" alt="{{ SITE_NAME }}" style="width:46px;height:46px;border-radius:12px;object-fit:cover;">
        <div>
          <div class="brand-name">UPSC<span>Notes</span></div>
          <div class="brand-tag">{{ SITE_TAGLINE }}</div>
        </div>
      </a>

      <form class="searchbar" action="{{ url_for('browse') }}" method="GET">
        <input type="text" name="q" placeholder="Search premium notes..." value="{{ request.args.get('q','') }}">
        <button type="submit">&#128269;</button>
      </form>

      <nav class="nav-links">
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('about') }}">About</a>
        <a href="{{ url_for('contact') }}">Contact</a>
        {% if is_user %}
          <a href="{{ url_for('user_dashboard') }}">👤 {{ current_user }}</a>
          <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
          <a href="{{ url_for('login') }}">Login</a>
          <a class="admin-btn" href="{{ url_for('signup') }}">Sign Up</a>
        {% endif %}
        {% if is_admin %}
          <a class="admin-btn" href="{{ url_for('admin_upload') }}">+ Upload</a>
          <a class="admin-btn" href="{{ url_for('admin_logout') }}">Admin Logout</a>
        {% else %}
          <a href="{{ url_for('admin_login') }}">Admin</a>
        {% endif %}
        <button class="theme-toggle" id="themeToggle" title="Dark/Light">&#127769;</button>
      </nav>
    </div>
  </header>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flashes">
        {% for cat, msg in messages %}
          <div class="flash {{ cat }}">{{ msg }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  {% block content %}{% endblock %}

  <script>
    (function() {
      var btn = document.getElementById('themeToggle');
      var saved = null;
      try { saved = localStorage.getItem('upsc_theme'); } catch(e) {}
      function apply(t) {
        document.body.classList.toggle('dark-mode', t === 'dark');
        if (btn) btn.textContent = t === 'dark' ? '☀️' : '🌙';
      }
      if (saved) apply(saved);
      if (btn) btn.addEventListener('click', function() {
        var isDark = document.body.classList.contains('dark-mode');
        var next = isDark ? 'light' : 'dark';
        try { localStorage.setItem('upsc_theme', next); } catch(e) {}
        apply(next);
      });
    })();
  </script>

  <footer class="site">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4>{{ SITE_NAME }}</h4>
          <p style="font-size:14px;">UPSC &amp; State PCS exam ki taiyari ke liye curated premium notes.</p>
        </div>
        <div>
          <h4>Quick Links</h4>
          <a href="{{ url_for('index') }}">Home</a>
          <a href="{{ url_for('about') }}">About Us</a>
          <a href="{{ url_for('contact') }}">Contact</a>
        </div>
        <div>
          <h4>Subjects</h4>
          {% for s in all_subjects[:5] %}
            <a href="{{ url_for('subject_page', slug=s.slug) }}">{{ s.name }}</a>
          {% endfor %}
        </div>
      </div>
      <div class="copy">&#169; {{ now_year() }} {{ SITE_NAME }} &#8212; Sabhi adhikaar surakshit.
        <br><span style="color:#e6c25c;font-weight:700;letter-spacing:1px;">&#9889; Powered by ANUJ IAS ASPIRANT &#9889;</span>
      </div>
    </div>
  </footer>

</body>
</html>
""",
    'browse.html': """{% extends "base.html" %}
{% block title %}All Notes — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>📖 Saare Notes</h2>
    <p>Filter karke apni zaroorat ke notes dhoondein.</p>
  </div>

  <!-- Filter bar -->
  <form class="filter-bar" method="GET" action="{{ url_for('browse') }}">
    <input type="text" name="q" placeholder="Search notes..." value="{{ q }}" style="flex:1;min-width:200px;">
    <select name="subject">
      <option value="">Sab subjects</option>
      {% for s in all_subjects %}
        <option value="{{ s.slug }}" {% if subject == s.slug %}selected{% endif %}>{{ s.name }}</option>
      {% endfor %}
    </select>
    <select name="sort">
      <option value="new" {% if sort=='new' %}selected{% endif %}>Newest</option>
      <option value="price_low" {% if sort=='price_low' %}selected{% endif %}>Price: Low to High</option>
      <option value="price_high" {% if sort=='price_high' %}selected{% endif %}>Price: High to Low</option>
    </select>
    <button class="btn btn-primary" type="submit">Filter 🔍</button>
  </form>

  {% if notes %}
    <div class="note-grid">
      {% for n in notes %}
        {% include "_note_card.html" %}
      {% endfor %}
    </div>
  {% else %}
    <div class="card" style="text-align:center; padding:50px;">
      <div style="font-size:50px;">🔍</div>
      <h3>Koi notes nahi mile</h3>
      <p>Apna search badal kar dobara try karein.</p>
      <a href="{{ url_for('browse') }}" class="btn btn-primary">Clear Filters</a>
    </div>
  {% endif %}
</div>
{% endblock %}
""",
    'buy.html': """{% extends "base.html" %}
{% block title %}Buy — {{ note.title }}{% endblock %}

{% block content %}
<div class="container">
  <div class="breadcrumb">
    <a href="{{ url_for('note_detail', note_id=note.id) }}">← Note pe wapas</a>
  </div>

  <div class="detail-wrap">
    <div class="detail-main">
      <h2 style="margin-top:0;">✅ Order Summary</h2>
      <div class="card">
        <div class="list-keyval">
          <div><span>Note</span><b>{{ note.title }}</b></div>
          <div><span>Subject</span><b>{{ subject_emoji(note.subject_slug) }} {{ subject_name(note.subject_slug) }}</b></div>
          <div><span>Format</span><b>{{ note.file_type|upper }}</b></div>
          <div><span>Total</span><b class="price" style="font-size:22px;">₹{{ '%g' % note.price }}</b></div>
        </div>

        <h3>📲 Payment Kaise Karein?</h3>
        <ol style="color:var(--muted); line-height:2;">
          <li><b>UPI QR scan</b> karke payment karein (₹{{ '%g' % note.price }})</li>
          <li>Payment <b>Screenshot</b> save karein</li>
          <li>Payment ka <b>reference/UTR number</b> note kar lein</li>
          <li>Hamein <b>WhatsApp/Call/Email</b> par screenshot bhejein</li>
          <li>Verify hone ke baad aapko notes ki <b>full copy</b> mil jayegi</li>
        </ol>

        <p style="font-size:14px; color:var(--muted);">Payment ke baad notes turant deliver kiya jayega — usually 5–30 minute ke andar.</p>
      </div>
    </div>

    <div class="buy-box card" style="text-align:center;">
      <h3 style="margin-top:0;">💳 UPI Payment</h3>
      <a href="{{ url_for('pay_order', note_id=note.id) }}" class="btn btn-gold" style="width:100%; font-size:16px; margin-bottom:14px;">💳 Pay with Razorpay (Test)</a>
      <div style="font-size:12px;color:var(--muted); margin-bottom:14px;">— ya UPI se pay karein —</div>
      {% if qr %}
        <img src="{{ qr }}" alt="UPI QR" style="width:200px;height:200px;object-fit:contain;border:1px solid var(--border);border-radius:12px;">
        <p style="font-size:13px;color:var(--muted);margin:8px 0;">Scan karke ₹{{ '%g' % note.price }} bharein</p>
      {% else %}
        <div style="font-size:70px;">📲</div>
        <p style="color:var(--muted);">QR code abhi add nahi kiya gaya. UPI ID se bhej sakte hain.</p>
      {% endif %}
      <div style="background:var(--bg);border-radius:10px;padding:12px;margin:14px 0;">
        <div style="font-size:13px;color:var(--muted);">UPI ID</div>
        <b style="font-size:18px;">{{ UPI_ID }}</b>
      </div>

      <a href="https://wa.me/{{ SELLER_WHATSAPP|replace('+','') }}" class="btn btn-accent" style="width:100%;" target="_blank">💬 WhatsApp par Payment Bhejein</a>
      <a href="tel:{{ SELLER_PHONE }}" class="btn btn-ghost" style="width:100%; margin-top:10px;">📞 Call Karein</a>
      <a href="mailto:{{ SELLER_EMAIL }}" class="btn btn-ghost" style="width:100%; margin-top:10px;">✉️ Email Karein</a>
      <p style="font-size:12px;color:var(--muted);margin-top:14px;">Payment bhejne ke baad screen shot bhejna na bhoolein!</p>
    </div>
  </div>
</div>
{% endblock %}
""",
    'buy_success.html': """{% extends "base.html" %}
{% block title %}Payment Success — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="card" style="max-width:560px; margin:40px auto; text-align:center;">
    <div style="font-size:70px;">✅</div>
    <h2 style="margin:10px 0;">Payment Successful!</h2>
    <p style="color:var(--muted);">Aapki payment ho gayi hai. Notes aapko jald hi milenge.</p>
    {% if note %}
    <div class="list-keyval" style="text-align:left;">
      <div><span>Note</span><b>{{ note.title }}</b></div>
      <div><span>Payment ID</span><b>{{ payment_id }}</b></div>
      <div><span>Amount</span><b class="price">₹{{ '%g' % note.price }}</b></div>
    </div>
    {% endif %}
    <div style="margin-top:20px;">
      <a href="{{ url_for('browse') }}" class="btn btn-gold">📖 Aur Notes Dekhein</a>
      <a href="{{ url_for('index') }}" class="btn btn-ghost">🏠 Home</a>
    </div>
  </div>
</div>
{% endblock %}
""",
    'contact.html': """{% extends "base.html" %}
{% block title %}Contact — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title"><h2>Contact Us</h2></div>
  <div class="card" style="max-width:700px;">
    <p style="color:var(--muted);">Koi sawaal ho, ya note kharidne mein help chahiye, toh humse contact karein:</p>
    <div class="list-keyval">
      <div><span>📧 Email</span><b>{{ SELLER_EMAIL }}</b></div>
      <div><span>💬 WhatsApp</span><b>{{ SELLER_WHATSAPP }}</b></div>
    </div>
    <a href="mailto:{{ SELLER_EMAIL }}" class="btn btn-primary">✉️ Email Bhejein</a>
    <a href="https://wa.me/{{ SELLER_WHATSAPP|replace('+','') }}" class="btn btn-accent" target="_blank">💬 WhatsApp Karein</a>
  </div>
</div>
{% endblock %}
""",
    'index.html': """{% extends "base.html" %}
{% block title %}{{ SITE_NAME }} — Premium UPSC Notes{% endblock %}

{% block content %}

<!-- Hero -->
<section class="hero">
  <div class="container">
    <span class="hero-badge">✦ Premium Edition · UPSC · BPSC · State PCS ✦</span>
    <h1>Premium UPSC Notes<br><span class="grad-text">One Destination, Every Subject</span></h1>
    <p>Expert-curated cheatsheets crafted for Prelims &amp; Mains — Geography, Polity, History, Economics, Science &amp; Tech aur bahut kuch.</p>
    <div class="cta">
      <a href="{{ url_for('browse') }}" class="btn btn-gold">✨ Explore Premium Notes</a>
      <a href="#subjects" class="btn btn-line">🗂️ Browse Subjects</a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><div class="num">{{ total_notes }}</div><div class="lbl">Notes</div></div>
      <div class="hero-stat"><div class="num">{{ bundle_count }}</div><div class="lbl">Bundles</div></div>
      <div class="hero-stat"><div class="num">{{ subject_count }}</div><div class="lbl">Subjects</div></div>
    </div>
  </div>
</section>

<div class="container">

  <!-- Subjects -->
  <div class="section-title" id="subjects">
    <div class="tag">Explore</div>
    <h2>Browse by <em>Subject</em></h2>
    <p>Apne subject par click karke notes dekhein.</p>
  </div>
  <div class="subject-grid">
    {% for s in subject_counts %}
      <div class="subject-card">
        <a href="{{ url_for('subject_page', slug=s.slug) }}">
          <span class="emoji">{{ subject_emoji(s.slug) }}</span>
          <span class="name">{{ s.name }}</span>
          <span class="count">{{ s.hindi }} · {{ s.cnt }} notes</span>
          <span class="exam-tag">📝 Prelims + Mains</span>
        </a>
        {% if s.bundle_id and s.bundle_price > 0 %}
          <a href="{{ url_for('buy_note', note_id=s.bundle_id) }}" class="btn btn-gold" style="margin-top:12px;width:100%;padding:10px;font-size:14px;">🛒 Buy ₹{{ '%g' % s.bundle_price }}</a>
        {% else %}
          <a href="{{ url_for('subject_page', slug=s.slug) }}" class="btn btn-ghost" style="margin-top:12px;width:100%;padding:10px;font-size:14px;">🗂️ Open</a>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <!-- UPSC OPTIONAL -->
  <div class="optional-section">
    <button class="optional-toggle" id="optionalToggle" onclick="toggleOptional()">
      <span class="opt-emoji">🎓</span>
      <span>UPSC Optional Subjects</span>
      <span class="opt-hint">👇 Click karke dekhein — sabse popular optional: Geography</span>
    </button>
    <div class="optional-panel" id="optionalPanel">
      <h3>🎓 UPSC <em>Optional Subject</em></h3>
      <div class="optional-grid">
        <a class="optional-card featured" href="{{ url_for('subject_page', slug='geography-optional') }}">
          <span class="emoji">🌍</span>
          <span class="tag">⭐ UPSC Optional</span>
          <span class="name">Geography Optional</span>
        </a>
      </div>
    </div>
  </div>
  <script>
    function toggleOptional() {
      var panel = document.getElementById('optionalPanel');
      var btn = document.getElementById('optionalToggle');
      panel.classList.toggle('open');
      btn.querySelector('.opt-hint').textContent =
        panel.classList.contains('open') ? '▲ Click karke band karein' : '👇 Click karke dekhein — sabse popular optional: Geography';
    }
  </script>

  <!-- Features -->
  <div class="feature-grid">
    <div class="feature-card"><div class="ico">📄</div><h3>PDF & HTML</h3><p>Easy to read &amp; print</p></div>
    <div class="feature-card"><div class="ico">🎯</div><h3>Exam-Focused</h3><p>Prelims + Mains</p></div>
    <div class="feature-card"><div class="ico">💳</div><h3>Secure UPI</h3><p>QR scan karke</p></div>
    <div class="feature-card"><div class="ico">⚡</div><h3>Instant Access</h3><p>Turant delivery</p></div>
  </div>

  <!-- TRUST / MINDSET -->
  <div class="trust-section">
    <div class="trust-badge">👥 <span class="tnum">5 Lakh+</span> Trusted Students</div>
    <p style="color:var(--muted); max-width:620px; margin:14px auto;">UPSC aspirants ka apna parivaar — jo hum par bharosa karke apne sapne poore kar rahe hain.</p>
    <div class="trust-stats">
      <div class="trust-card"><div class="ico">🎯</div><div class="num">5L+</div><div class="lbl">Trusted Students</div></div>
      <div class="trust-card"><div class="ico">📚</div><div class="num">365+</div><div class="lbl">Premium Notes</div></div>
      <div class="trust-card"><div class="ico">🏅</div><div class="num">99%</div><div class="lbl">Success Rate</div></div>
      <div class="trust-card"><div class="ico">⭐</div><div class="num">4.9/5</div><div class="lbl">Student Rating</div></div>
    </div>
    <div class="trust-quote">
      <p>"Sapne dekhne se nahi, sapno par bharosa rakhne se pure hote hain. Hamare 5 lakh+ students ka bharosa hi hamari asli kamai hai."</p>
      <div class="by">✨ ANUJ IAS ASPIRANT ✨</div>
    </div>
  </div>

  <!-- Featured -->
  {% if featured %}
    <div class="section-title">
      <div class="tag">Best Sellers</div>
      <h2>Featured <em>Bundles</em></h2>
      <p>Hamari sabse popular notes — complete bundles.</p>
    </div>
    <div class="note-grid">
      {% for n in featured %}
        {% include "_note_card.html" %}
      {% endfor %}
    </div>
  {% endif %}

  <!-- CTA -->
  <div class="cta-banner">
    <h2>Unlock Your Full Potential</h2>
    <p>Complete bundles mein saare notes ek saath — better price, better preparation.</p>
    <a href="{{ url_for('browse') }}" class="btn btn-gold">🛒 Start Learning Now</a>
  </div>

  <!-- NEON QUOTE -->
  <div class="quote-section">
    <div class="quote-box">
      <div class="quote-mark">"</div>
      <div class="quote-text" id="quoteText">कठिन परिश्रम का कोई विकल्प नहीं है। अपनी मेहनत, समर्पण और सपनों पर विश्वास रखो — कामयाबी ज़रूर मिलेगी।</div>
      <div class="quote-author" id="quoteAuthor">✨ UPSC Aspirants ✨</div>
    </div>
  </div>
  <script>
    (function() {
      var quotes = [
        { text: "कठिन परिश्रम का कोई विकल्प नहीं है। अपनी मेहनत, समर्पण और सपनों पर विश्वास रखो — कामयाबी ज़रूर मिलेगी।", author: "✨ UPSC Aspirants ✨" },
        { text: "सपने वो नहीं जो सोने पर आते हैं, सपने वो हैं जो सोने नहीं देते।", author: "✨ Dr. A.P.J. Abdul Kalam ✨" },
        { text: "सफलता कोई संयोग नहीं है, यह कठिन परिश्रम, दृढ़ इच्छाशक्ति और अटूट विश्वास का परिणाम है।", author: "✨ Aspirant's Mantra ✨" },
        { text: "जो सपने देखते हैं और उन्हें पूरा करने के लिए ज़िंदगी दाँव पर लगाते हैं, उन्हीं की जीत होती है।", author: "✨ UPSC Journey ✨" },
        { text: "हार मान लेना आसान है, लेकिन मंज़िल उन्हीं को मिलती है जो हर असफलता के बाद नए सिरे से शुरू करते हैं।", author: "✨ Never Give Up ✨" }
      ];
      var idx = 0;
      function show() {
        var t = document.getElementById('quoteText');
        var a = document.getElementById('quoteAuthor');
        if (t && a) {
          t.style.opacity = 0;
          a.style.opacity = 0;
          setTimeout(function() {
            t.textContent = quotes[idx].text;
            a.textContent = quotes[idx].author;
            t.style.opacity = 1;
            a.style.opacity = 1;
          }, 300);
        }
        idx = (idx + 1) % quotes.length;
      }
      setInterval(show, 6000);
    })();
  </script>


</div>
{% endblock %}
""",
    'library.html': """{% extends "base.html" %}
{% block title %}My Library — {{ bundle.title }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>📚 {{ subject_name(bundle.subject_slug) }} — Saari Files</h2>
    <p>Neeche aapki khareedi hui bundle ki saari files chapter-wise hain. Har file open/download karein.</p>
  </div>

  <div class="flash success" style="margin:0 0 20px;">✅ Aapke paas is bundle ka poora access hai. Saari files free mein available hain.</div>

  {% if files %}
    <table class="admin-table">
      <thead>
        <tr><th>#</th><th>Chapter / Topic</th><th style="width:180px;">Actions</th></tr>
      </thead>
      <tbody>
        {% for f in files %}
        <tr>
          <td>{{ loop.index }}</td>
          <td><b>{{ f.title }}</b></td>
          <td>
            <a href="{{ url_for('note_view', note_id=f.id) }}" class="btn btn-sm btn-ghost" target="_blank">👁️ Open</a>
            <a href="{{ url_for('download_note', note_id=f.id) }}" class="btn btn-sm btn-gold">⬇️ Download</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <div class="card" style="text-align:center;padding:40px;">📭 Is bundle mein koi file nahi hai.</div>
  {% endif %}

  <div style="text-align:center;margin-top:24px;">
    <a href="{{ url_for('browse') }}" class="btn btn-gold">📖 Aur Notes Dekhein</a>
    <a href="{{ url_for('user_dashboard') }}" class="btn btn-ghost">👤 My Account</a>
  </div>
</div>
{% endblock %}
""",
    'login.html': """{% extends "base.html" %}
{% block title %}Login — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="auth-wrap">
  <div class="card">
    <div style="text-align:center; margin-bottom:20px;">
      <div style="font-size:50px;">🔐</div>
      <h2 style="margin:8px 0 4px;">Login Karein</h2>
      <p style="color:var(--muted); margin:0; font-size:14px;">Apne account se login karein.</p>
    </div>
    <form method="POST">
      <input type="hidden" name="next" value="{{ next_url }}">
      <div class="form-group">
        <label>Email</label>
        <input type="email" name="email" required placeholder="you@example.com">
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" name="password" required placeholder="••••••••">
      </div>
      <button type="submit" class="btn btn-primary" style="width:100%;">Login</button>
    </form>
    <p style="text-align:center; font-size:14px; color:var(--muted); margin-top:16px;">
      Account nahi hai? <a href="{{ url_for('signup') }}"><b>Sign up karein</b></a>
    </p>
  </div>
</div>
{% endblock %}
""",
    'note_detail.html': """{% extends "base.html" %}
{% block title %}{{ note.title }} — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="breadcrumb">
    <a href="{{ url_for('index') }}">Home</a> /
    <a href="{{ url_for('subject_page', slug=note.subject_slug) }}">{{ subject_name(note.subject_slug) }}</a> /
    {{ note.title }}
  </div>

  <div class="detail-wrap">
    <div class="detail-main">
      <div class="note-thumb">
        {% if note.file_type == 'pdf' %}📄{% else %}🌐{% endif %}
        <span class="type-badge">{{ note.file_type|upper }}</span>
        {% if note.featured %}<span class="badge-featured" style="position:absolute;left:10px;top:10px;">⭐ Featured</span>{% endif %}
      </div>

      <h1 class="detail-title">{{ note.title }}</h1>

      <div class="list-keyval">
        <div><span>Subject</span><b>{{ subject_emoji(note.subject_slug) }} {{ subject_name(note.subject_slug) }}</b></div>
        <div><span>File Type</span><b>{{ note.file_type|upper }}</b></div>
        {% if note.pages %}<div><span>Pages</span><b>{{ note.pages }}</b></div>{% endif %}
        <div><span>Language</span><b>{{ note.language }}</b></div>
        <div><span>Uploaded</span><b>{{ note.created_at }}</b></div>
        <div><span>Price</span>
          <b>
            <span class="price">₹{{ '%g' % note.price }}</span>
            {% if note.original_price and note.original_price > note.price %}
              <span class="orig-price">₹{{ '%g' % note.original_price }}</span>
            {% endif %}
          </b>
        </div>
      </div>

      <h3 style="margin-bottom:6px;">📝 Description</h3>
      <p style="color:var(--muted); white-space:pre-line;">{{ note.description or 'Koi description nahi diya gaya.' }}</p>

      <div class="toolbar">
        {% if note.id in demo_preview_ids or is_admin %}
          <a href="{{ url_for('note_view', note_id=note.id) }}" class="btn btn-ghost" target="_blank">👁️ Preview</a>
        {% endif %}
        {% if is_admin %}
          <a href="{{ url_for('download_note', note_id=note.id) }}" class="btn btn-gold" target="_blank">⬇️ Free Download</a>
          <form method="post" action="{{ url_for('admin_delete', note_id=note.id) }}" onsubmit="return confirm('Kya aap ye note delete karna chahte hain?');">
            <button class="btn btn-danger" type="submit">🗑️ Delete</button>
          </form>
        {% endif %}
      </div>
    </div>

    <!-- Buy box -->
    <div class="buy-box card">
      <h3 style="margin-top:0;">🛒 Purchase Karin</h3>
      <div class="price-row">
        <span class="price" style="font-size:32px;">₹{{ '%g' % note.price }}</span>
        {% if note.original_price and note.original_price > note.price %}
          <span class="orig-price" style="font-size:16px;">₹{{ '%g' % note.original_price }}</span>
        {% endif %}
      </div>
      <p style="color:var(--muted);font-size:14px;">Payment hone ke baad aapko notes ki full copy mil jayegi.</p>
      <a href="{{ url_for('buy_note', note_id=note.id) }}" class="btn btn-accent" style="width:100%; text-align:center; font-size:16px;">🛒 Abhi Kharidein</a>
      <hr style="margin:18px 0; border:none; border-top:1px solid var(--border);">
      <div class="list-keyval">
        <div><span>Payment</span><b>UPI / Bank</b></div>
        <div><span>Delivery</span><b>Instant (online)</b></div>
        <div><span>Format</span><b>{{ note.file_type|upper }}</b></div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
""",
    'pay.html': """{% extends "base.html" %}
{% block title %}Payment — {{ note.title }}{% endblock %}

{% block content %}
<div class="container">
  <div class="detail-wrap">
    <div class="detail-main">
      <div class="card">
        <h2>💳 Razorpay Test Payment</h2>
        {% if RAZORPAY_TEST_MODE %}
          <div class="flash info" style="margin:0 0 16px;">⚠️ Ye TEST mode hai — koi real payment nahi hota. Testing ke liye use karein.</div>
        {% endif %}
        <div class="list-keyval">
          <div><span>Note</span><b>{{ note.title }}</b></div>
          <div><span>Amount</span><b class="price">₹{{ '%g' % note.price }}</b></div>
        </div>
        <p style="color:var(--muted);">"Pay" button dabao → Razorpay test popup → koi bhi test card/UPI use karo → payment success.</p>
        <button id="rzp-button" class="btn btn-gold" style="width:100%;font-size:17px;">💳 Pay ₹{{ '%g' % note.price }} (Test)</button>
      </div>
    </div>
  </div>
</div>

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
  var options = {
    key: "{{ key_id }}",
    amount: {{ order['amount'] }},
    currency: "{{ order['currency'] }}",
    name: "UPSC Notes Store",
    description: "{{ note.title }}",
    order_id: "{{ order['id'] }}",
    handler: function (response) {
      // payment success par verify route par bhejo
      var form = document.createElement('form');
      form.method = 'POST';
      form.action = "{{ url_for('pay_verify') }}";
      var fields = {
        razorpay_payment_id: response.razorpay_payment_id,
        razorpay_order_id: response.razorpay_order_id,
        razorpay_signature: response.razorpay_signature,
        note_id: "{{ note.id }}"
      };
      for (var k in fields) {
        var i = document.createElement('input');
        i.type = 'hidden'; i.name = k; i.value = fields[k];
        form.appendChild(i);
      }
      document.body.appendChild(form);
      form.submit();
    },
    modal: { ondismiss: function(){ alert("Payment cancel ho gaya. Dobara try karein."); } }
  };
  document.getElementById('rzp-button').onclick = function(e) {
    var rzp = new Razorpay(options);
    rzp.open();
    e.preventDefault();
  };
</script>
{% endblock %}
""",
    'preview.html': """{% extends "base.html" %}
{% block title %}Preview — {{ bundle.title }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>👁️ {{ subject_name(bundle.subject_slug) }} — Preview</h2>
    <p>Neeche subject ke saare topics hain aur pehli file ka sample content.</p>
  </div>

  <!-- Child parts (jaise History ke 5 parts) -->
  {% if child_parts %}
    <div class="section-title">
      <h2>🗂️ {{ subject_name(bundle.subject_slug) }} ke Bhag</h2>
      <p>Har part ka ek preview file neeche open hota hai.</p>
    </div>
    <div class="subject-grid">
      {% for c in child_parts %}
        <a class="subject-card" href="{{ url_for('subject_page', slug=c.slug) }}">
          <span class="emoji">{{ subject_emoji(c.slug) }}</span>
          <span class="name">{{ c.name }}</span>
          <span class="count">{{ c.hindi }} · {{ c.count }} files</span>
          <span class="exam-tag">👁️ Preview Available</span>
        </a>
      {% endfor %}
    </div>
  {% endif %}

  <div class="detail-wrap">
    <!-- Topics list -->
    <div class="card" style="position:sticky;top:90px;max-height:80vh;overflow:auto;">
      <h3 style="margin-top:0;">📚 {{ subject_name(bundle.subject_slug) }} ke Topics</h3>
      {% if topics %}
      <ol style="padding-left:20px; line-height:2;">
        {% for t in topics %}
          <li>{{ t.title }}</li>
        {% endfor %}
      </ol>
      {% else %}
        <p style="color:var(--muted);">Is subject ke parts mein files hain — upar parts dekhein.</p>
      {% endif %}
    </div>

    <!-- First file content -->
    <div class="detail-main">
      <!-- Child parts previews (har part ki ek file) -->
      {% if child_parts and not purchased %}
        <h3>📄 Har Part ki Ek Preview File</h3>
        {% for c in child_parts %}
          {% if c.preview_file %}
            <div style="border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:#fff;margin-bottom:20px;">
              <div style="padding:10px 16px;background:var(--grad-emerald);color:#fff;font-weight:700;">{{ subject_emoji(c.slug) }} {{ c.name }} — Preview</div>
              <iframe src="data:text/html;base64,{{ c.preview_file.content|default('') }}" style="width:100%;min-height:500px;border:none;"></iframe>
            </div>
          {% endif %}
        {% endfor %}
        <div style="text-align:center;margin-bottom:16px;">
          <a href="{{ url_for('buy_note', note_id=bundle.id) }}" class="btn btn-gold">🛒 Poora Bundle Kharidein (₹{{ '%g' % bundle.price }})</a>
        </div>
      {% endif %}

      {% if purchased %}
        <div class="flash success" style="margin:0 0 16px;">✅ Aapne ye bundle kharid liya hai! Saari files neeche chapter-wise available hain.</div>
        <div style="text-align:center;margin-bottom:16px;">
          <a href="{{ url_for('library', bundle_id=bundle.id) }}" class="btn btn-gold">📖 Pura Bundle Kholo (Saari Files)</a>
        </div>
      {% else %}
        <div class="flash info" style="margin:0 0 16px;">👁️ Ye sirf PREVIEW hai — pehli file ka sample. Poora bundle kharidne ke liye <b>🛒 Buy</b> dabayein.</div>
      {% endif %}
      {% if first_content %}
        <div style="border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:#fff;">
          <iframe src="data:text/html;base64,{{ first_content }}" style="width:100%;min-height:700px;border:none;"></iframe>
        </div>
      {% else %}
        <div class="card" style="text-align:center;padding:40px;">📭 Is subject ki files abhi upload nahi hui.</div>
      {% endif %}
      {% if purchased %}
        <div style="text-align:center;margin-top:20px;">
          <a href="{{ url_for('note_view', note_id=bundle.id) }}" class="btn btn-gold" target="_blank">📖 Pura Bundle Kholo (Saari Files)</a>
        </div>
      {% else %}
        <div style="text-align:center;margin-top:20px;">
          <a href="{{ url_for('buy_note', note_id=bundle.id) }}" class="btn btn-gold">🛒 Poora Bundle Kharidein (₹{{ '%g' % bundle.price }})</a>
        </div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
""",
    'signup.html': """{% extends "base.html" %}
{% block title %}Sign Up — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="auth-wrap">
  <div class="card">
    <div style="text-align:center; margin-bottom:20px;">
      <div style="font-size:50px;">✨</div>
      <h2 style="margin:8px 0 4px;">Account Banayein</h2>
      <p style="color:var(--muted); margin:0; font-size:14px;">Notes kharidne ke liye account banao.</p>
    </div>
    <form method="POST">
      <input type="hidden" name="next" value="{{ next_url }}">
      <div class="form-group">
        <label>Apna Naam</label>
        <input type="text" name="name" required placeholder="e.g. Rahul Kumar">
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" name="email" required placeholder="you@example.com">
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" name="password" required placeholder="••••••••">
      </div>
      <div class="form-group">
        <label>Confirm Password</label>
        <input type="password" name="confirm" required placeholder="••••••••">
      </div>
      <button type="submit" class="btn btn-primary" style="width:100%;">Create Account</button>
    </form>
    <p style="text-align:center; font-size:14px; color:var(--muted); margin-top:16px;">
      Pehle se account hai? <a href="{{ url_for('login') }}"><b>Login karein</b></a>
    </p>
  </div>
</div>
{% endblock %}
""",
    'subject.html': """{% extends "base.html" %}
{% block title %}{{ subject.name }} Notes — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>{{ subject_emoji(subject.slug) }} {{ subject.name }} Notes <span style="font-size:16px;color:var(--muted);font-weight:400">({{ subject.hindi }})</span></h2>
    <p>{{ notes|length }} notes is subject mein available.</p>
  </div>

  {% if children %}
    <div class="section-title" style="margin-top:24px;">
      <div class="tag">Sub-Parts</div>
      <h2>🗂️ {{ subject.name }} ke Bhag</h2>
      <p>Har part ko alag se buy ya preview karein.</p>
    </div>
    <div class="note-grid">
      {% for c in children %}
        <div class="note-card">
          <div class="note-thumb"><span style="font-size:50px;">{{ subject_emoji(c.slug) }}</span></div>
          <div class="note-body">
            <span class="subject-tag">{{ subject_emoji(c.slug) }} {{ c.name }}</span>
            <h3><a href="{{ url_for('subject_page', slug=c.slug) }}">{{ c.name }}</a></h3>
            <p class="note-desc">{{ c.hindi }} · {{ c.count }} files</p>
            {% if c.price and c.price > 0 %}
              <div class="price-row">
                <span class="price">₹{{ '%g' % c.price }}</span>
                {% if c.orig_price and c.orig_price > c.price %}<span class="orig-price">₹{{ '%g' % c.orig_price }}</span>{% endif %}
              </div>
            {% endif %}
            <div class="note-actions">
              {% if c.first_file_id %}
                <a href="{{ url_for('note_view', note_id=c.first_file_id) }}" class="btn btn-ghost" target="_blank">👁️ Preview</a>
              {% elif c.bundle_id %}
                <a href="{{ url_for('note_view', note_id=c.bundle_id) }}" class="btn btn-ghost" target="_blank">👁️ Preview</a>
              {% endif %}
              {% if c.bundle_id %}
                <a href="{{ url_for('buy_note', note_id=c.bundle_id) }}" class="btn btn-primary">🛒 Buy</a>
              {% else %}
                <a href="{{ url_for('subject_page', slug=c.slug) }}" class="btn btn-ghost">🗂️ Open</a>
              {% endif %}
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  {% endif %}

  {% if notes %}
    <div class="note-grid">
      {% for n in notes %}
        {% include "_note_card.html" %}
      {% endfor %}
    </div>
  {% elif not children %}
    <div class="card" style="text-align:center; padding:50px;">
      <div style="font-size:50px;">📭</div>
      <h3>Is subject mein abhi notes nahi hain</h3>
      <p>Jald hi aayenge. Tab tak doosre subjects check karein.</p>
    </div>
  {% endif %}
</div>
{% endblock %}
""",
}
