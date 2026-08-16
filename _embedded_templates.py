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
    'admin_base.html': """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{% block title %}ANUJ Admin{% endblock %}</title>
  <meta name="description" content="Admin App — ANUJ IAS ASPIRANT">
  <meta name="robots" content="noindex, nofollow">
  <!-- PWA -->
  <link rel="manifest" href="{{ url_for('admin_manifest') }}">
  <meta name="theme-color" content="#2d0d66">
  <link rel="icon" href="{{ url_for('static', filename='aw-logo-192.png') }}">
  <link rel="apple-touch-icon" href="{{ url_for('static', filename='aw-logo-192.png') }}">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <style>
    :root{
      --purple:#6c2bd9; --purple-dark:#4b1a9e; --deep:#2d0d66;
      --gold:#c9a227; --ink:#1a1130; --muted:#6b5f85;
      --cream:#f8f6fc; --card:#fff; --line:rgba(108,43,217,.12);
      --red:#dc2626; --green:#16a34a;
    }
    *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
    html,body{margin:0;padding:0;}
    body{
      font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--cream);
      color:var(--ink);padding-bottom:76px; /* space for bottom nav */
    }
    .appbar{
      position:sticky;top:0;z-index:50;background:linear-gradient(135deg,var(--purple),var(--deep));
      color:#fff;padding:16px 16px;display:flex;align-items:center;gap:12px;
      box-shadow:0 4px 18px rgba(45,13,102,.3);
    }
    .appbar img{width:40px;height:40px;border-radius:10px;background:#fff;}
    .appbar .t{font-weight:800;font-size:18px;letter-spacing:.3px;}
    .appbar .s{font-size:12px;opacity:.8;}
    .appbar .spacer{flex:1;}
    .appbar .exit{background:rgba(255,255,255,.15);border:none;color:#fff;padding:8px 12px;border-radius:9px;font-size:13px;font-weight:700;}
    .container{padding:16px;max-width:560px;margin:0 auto;}
    .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin-bottom:16px;box-shadow:0 2px 10px rgba(45,13,102,.06);}
    .card h3{margin:0 0 10px;}
    .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:16px;}
    .tile{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;text-align:center;box-shadow:0 2px 10px rgba(45,13,102,.06);}
    .tile .num{font-size:30px;font-weight:800;color:var(--purple);}
    .tile .lbl{font-size:12px;color:var(--muted);}
    .btn{display:inline-block;padding:13px 18px;border:none;border-radius:12px;font-weight:700;font-size:15px;cursor:pointer;text-decoration:none!important;text-align:center;}
    .btn-p{background:linear-gradient(135deg,var(--purple),var(--deep));color:#fff;box-shadow:0 4px 14px rgba(108,43,217,.35);}
    .btn-g{background:linear-gradient(120deg,#e6c25c,#c9a227);color:#2a1d00;box-shadow:0 4px 14px rgba(201,162,39,.35);}
    .btn-ghost{background:rgba(108,43,217,.08);color:var(--purple);}
    .btn-r{background:#fee2e2;color:var(--red);}
    .btn-sm{padding:9px 13px;font-size:13px;border-radius:10px;}
    .full{width:100%;}
    .form-group{margin-bottom:14px;}
    .form-group label{display:block;font-weight:700;font-size:13px;margin-bottom:6px;color:var(--ink);}
    .form-group input,.form-group select,.form-group textarea{width:100%;padding:13px 14px;border:1px solid var(--line);border-radius:11px;font-size:15px;background:var(--card);font-family:inherit;}
    .flash{padding:12px 14px;border-radius:11px;margin-bottom:12px;font-weight:600;font-size:14px;}
    .flash.success{background:#e6f7ed;color:#14532d;}
    .flash.error{background:#fee2e2;color:#7f1d1d;}
    .flash.info{background:#e0f2fe;color:#0c4a6e;}
    .list-item{display:flex;align-items:center;gap:10px;padding:12px 4px;border-bottom:1px solid var(--line);}
    .list-item:last-child{border-bottom:none;}
    .list-item .grow{flex:1;min-width:0;}
    .list-item .ttl{font-weight:700;font-size:14px;word-break:break-word;}
    .list-item .sub{font-size:12px;color:var(--muted);}
    .actions{display:flex;gap:6px;flex-wrap:wrap;}
    .tag{display:inline-block;background:var(--purple);color:#fff;font-size:10px;font-weight:700;padding:3px 9px;border-radius:20px;text-transform:uppercase;letter-spacing:.5px;}
    .subject-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
    .subject-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 8px;text-align:center;text-decoration:none;color:var(--ink);display:block;overflow:visible;}
    .subject-card span{line-height:1;overflow:visible;display:block;}
    .subject-card .name{font-weight:700;font-size:13px;display:block;margin-top:4px;line-height:1.3;}
    .subject-card .count{font-size:11px;color:var(--muted);display:block;margin-top:2px;line-height:1.3;}
    /* bottom nav */
    .bottomnav{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;background:#fff;border-top:1px solid var(--line);box-shadow:0 -4px 16px rgba(45,13,102,.08);padding-bottom:env(safe-area-inset-bottom);}
    .bottomnav a{flex:1;text-align:center;padding:10px 4px 8px;font-size:10px;color:var(--muted);text-decoration:none;font-weight:700;}
    .bottomnav a .ic{font-size:20px;display:block;}
    .bottomnav a.on{color:var(--purple);}
    /* auth */
    .authwrap{max-width:400px;margin:0 auto;padding:20px;}
    .center{text-align:center;}
    .install-banner{background:#eef2ff;border:1px solid #c7d2fe;color:#3730a3;border-radius:12px;padding:12px 14px;margin-bottom:14px;font-size:13px;display:flex;align-items:center;gap:10px;}
    .install-banner button{background:#4f46e5;color:#fff;border:none;border-radius:9px;padding:8px 12px;font-weight:700;font-size:13px;white-space:nowrap;}
  </style>
</head>
<body>
  <div class="appbar">
    <img src="{{ url_for('static', filename='aw-logo.png') }}" alt="logo"
         onerror="this.src='{{ url_for('static', filename='aw-logo-192.png') }}';">
    <div>
      <div class="t">{% block appbar_title %}ANUJ Admin{% endblock %}</div>
      <div class="s">⚡ ANUJ IAS ASPIRANT</div>
    </div>
    <div class="spacer"></div>
    {% if is_admin %}<a href="{{ url_for('admin_logout') }}" class="exit">Logout</a>{% endif %}
  </div>

  <div class="container">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for cat, msg in messages %}<div class="flash {{ cat }}">{{ msg }}</div>{% endfor %}
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
  </div>

  {% if is_admin %}
  <nav class="bottomnav">
    <a href="{{ url_for('admin_dashboard') }}" class="{% if request.endpoint=='admin_dashboard' %}on{% endif %}"><span class="ic">🏠</span>Dashboard</a>
    <a href="{{ url_for('admin_upload') }}" class="{% if request.endpoint=='admin_upload' %}on{% endif %}"><span class="ic">➕</span>Upload</a>
    <a href="{{ url_for('admin_subjects') }}" class="{% if request.endpoint=='admin_subjects' %}on{% endif %}"><span class="ic">🗂️</span>Subjects</a>
    <a href="{{ url_for('admin_purchase') }}" class="{% if request.endpoint=='admin_purchase' %}on{% endif %}"><span class="ic">🎟️</span>Purchase</a>
  </nav>
  {% endif %}

  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function(){
        navigator.serviceWorker.register('{{ url_for('admin_sw') }}').catch(function(){});
      });
    }
    // Install app button
    let deferredPrompt = null;
    window.addEventListener('beforeinstallprompt', function(e){
      e.preventDefault(); deferredPrompt = e;
      var b = document.getElementById('installBtn');
      var banner = document.getElementById('installBanner');
      if (b) b.onclick = function(){ deferredPrompt.prompt(); };
      if (banner) banner.style.display='flex';
    });
  </script>
</body>
</html>
""",
    'admin_dashboard.html': """{% extends "admin_base.html" %}
{% block title %}Dashboard{% endblock %}
{% block appbar_title %}Dashboard{% endblock %}

{% block content %}
  <div class="grid">
    <div class="tile"><div class="num">{{ total_notes }}</div><div class="lbl">Total Notes</div></div>
    <div class="tile"><div class="num">{{ counts|length }}</div><div class="lbl">Subjects</div></div>
  </div>

  <div class="grid" style="grid-template-columns:repeat(2,1fr);">
    <a href="{{ url_for('admin_upload') }}" class="btn btn-p" style="text-align:center;">➕ Upload</a>
    <a href="{{ url_for('admin_purchase') }}" class="btn btn-g" style="text-align:center;">🎟️ Purchase</a>
  </div>

  <div class="card">
    <h3>🗂️ Subject Chunein</h3>
    <div class="subject-grid">
      {% for c in counts %}
        <a class="subject-card" href="#sub-{{ c.slug }}">
          <span style="font-size:24px;">{{ subject_emoji(c.slug) }}</span>
          <span class="name">{{ c.name }}</span>
          <span class="count">{{ c.cnt }} files</span>
        </a>
      {% endfor %}
    </div>
  </div>

  {% for slug, items in by_subject.items() %}
    <div style="margin-top:6px;">
      <h3 id="sub-{{ slug }}" style="margin:18px 0 8px;">
        {{ subject_emoji(slug) }} {{ subject_name(slug) }}
        <span style="font-size:13px;color:var(--muted);font-weight:400;">({{ items|selectattr('__meta__','undefined')|list|length }} files)</span>
      </h3>
      <div class="card" style="padding:6px 14px;">
        {% set ns = namespace(c=0) %}
        {% for n in items %}
          {% if n.__meta__ is defined %}
          {% else %}
            {% set ns.c = ns.c + 1 %}
            <div class="list-item">
              <div class="grow">
                <div class="ttl">{{ ns.c }}. {{ n.title }}</div>
                <div class="sub"><span class="tag">{{ n.file_type }}</span> ₹{{ '%g' % n.price }}</div>
              </div>
              <div class="actions">
                <a href="{{ url_for('note_view', note_id=n.id) }}" class="btn btn-sm btn-ghost" target="_blank">👁️</a>
                <a href="{{ url_for('download_note', note_id=n.id) }}" class="btn btn-sm btn-g" style="padding:9px 10px;">⬇️</a>
                <form method="post" action="{{ url_for('admin_delete', note_id=n.id) }}"
                      onsubmit="return confirm('Delete {{ n.title|e }}?');">
                  <button class="btn btn-sm btn-r" style="padding:9px 10px;">🗑️</button>
                </form>
              </div>
            </div>
          {% endif %}
        {% endfor %}
      </div>
    </div>
  {% endfor %}
{% endblock %}
""",
    'admin_login.html': """{% extends "admin_base.html" %}
{% block title %}Admin Login{% endblock %}
{% block appbar_title %}Admin Login{% endblock %}

{% block content %}
<div class="authwrap">
  <div class="center" style="margin-bottom:16px;">
    <img src="{{ url_for('static', filename='aw-logo.png') }}" alt="logo"
         style="width:72px;height:72px;border-radius:18px;"
         onerror="this.src='{{ url_for('static', filename='aw-logo-192.png') }}';">
    <h2 style="margin:10px 0 4px;">ANUJ Admin App</h2>
    <p style="color:var(--muted);margin:0;font-size:13px;">Notes upload/delete ke liye login karein 🔐</p>
  </div>

  <div class="card">
    <div class="install-banner" id="installBanner" style="display:none;">
      <span>📲 Is app ko phone pe install karein?</span>
      <button id="installBtn">Install</button>
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
      <button type="submit" class="btn btn-p full">🔓 Login</button>
    </form>
  </div>
</div>
{% endblock %}
""",
    'admin_purchase.html': """{% extends "admin_base.html" %}
{% block title %}Purchase Access{% endblock %}
{% block appbar_title %}🎟️ Purchase Access{% endblock %}

{% block content %}
  <div class="card">
    <p style="margin:0 0 12px;color:var(--muted);font-size:13px;">UPI/manual payment confirm hone par user ka email + bundle select karke access dein.</p>
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
      <button type="submit" class="btn btn-g full">✅ Access Denein</button>
    </form>
  </div>
{% endblock %}
""",
    'admin_subjects.html': """{% extends "admin_base.html" %}
{% block title %}Manage Subjects{% endblock %}
{% block appbar_title %}🗂️ Subjects{% endblock %}

{% block content %}
  <div class="card">
    <h3>Naya Subject Add Karein</h3>
    <form method="POST">
      <input type="hidden" name="action" value="add">
      <div class="form-group">
        <label>Name *</label>
        <input type="text" name="name" required placeholder="e.g. Disaster Management">
      </div>
      <div class="form-group">
        <label>Hindi Name</label>
        <input type="text" name="hindi" placeholder="e.g. आपदा प्रबंधन">
      </div>
      <div class="form-group">
        <label>Slug (URL) — khali chhodo, auto ban jayega</label>
        <input type="text" name="slug" placeholder="e.g. disaster-management">
      </div>
      <button class="btn btn-p full" type="submit">➕ Subject Add Karein</button>
    </form>
  </div>

  <h3>Subjects ({{ subjects|length }})</h3>
  <div class="card" style="padding:6px 14px;">
    {% for s in subjects %}
      <div class="list-item">
        <div class="grow">
          <div class="ttl">{{ subject_emoji(s.slug) }} {{ s.name }}</div>
          <div class="sub">{{ s.hindi }} · {{ s.slug }}</div>
        </div>
        <div class="actions">
          <form method="POST" onsubmit="return confirm('Subject {{ s.name|e }} delete karein?');">
            <input type="hidden" name="action" value="delete">
            <input type="hidden" name="id" value="{{ s.id }}">
            <button class="btn btn-sm btn-r">🗑️</button>
          </form>
        </div>
      </div>
    {% endfor %}
  </div>
  <p style="font-size:12px;color:var(--muted);">Note: subject mein notes ho to pehle notes delete karein tabhi subject delete hoga.</p>
{% endblock %}
""",
    'admin_upload.html': """{% extends "admin_base.html" %}
{% block title %}Upload Note{% endblock %}
{% block appbar_title %}➕ Upload Note{% endblock %}

{% block content %}
  <div class="card">
    <form method="POST" enctype="multipart/form-data">
      <div class="form-group">
        <label>Note ka Title *</label>
        <input type="text" name="title" required placeholder="e.g. Geography Complete Notes">
      </div>
      <div class="form-group">
        <label>Subject *</label>
        <select name="subject_slug" required>
          {% for s in subjects %}
            <option value="{{ s.slug }}">{{ subject_emoji(s.slug) }} {{ s.name }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="form-group">
        <label>Language</label>
        <input type="text" name="language" value="Hindi + English">
      </div>
      <div class="form-group">
        <label>Description</label>
        <textarea name="description" rows="3" placeholder="Is note mein kya-kya covered hai..."></textarea>
      </div>
      <div class="form-group">
        <label>Price (₹) *</label>
        <input type="number" name="price" step="0.01" min="0" required placeholder="99">
      </div>
      <div class="form-group">
        <label>Original Price (₹) — optional (discount dikhane ke liye)</label>
        <input type="number" name="original_price" step="0.01" min="0" placeholder="199">
      </div>
      <div class="form-group">
        <label>Pages (optional)</label>
        <input type="number" name="pages" min="0" placeholder="150">
      </div>
      <div class="form-group">
        <label>File * (.pdf ya .html)</label>
        <input type="file" name="file" accept=".pdf,.html,.htm" required>
      </div>
      <div class="form-group">
        <label style="display:flex;align-items:center;gap:8px;">
          <input type="checkbox" name="featured" value="1" style="width:auto;">
          ⭐ Featured note (homepage par dikhega)
        </label>
      </div>
      <div style="display:flex;gap:10px;margin-top:6px;">
        <button type="submit" class="btn btn-p full">📤 Upload Karin</button>
        <a href="{{ url_for('admin_dashboard') }}" class="btn btn-ghost">Cancel</a>
      </div>
    </form>
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
.subject-card .emoji {
  font-size: 38px; display: flex; align-items: center; justify-content: center;
  width: 100%; min-height: 52px; line-height: 1; margin-bottom: 10px;
  filter: drop-shadow(0 3px 6px rgba(0,0,0,.1));
  overflow: visible; padding: 2px 0;
}
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
.note-thumb span { line-height: 1; overflow: visible; }
.note-thumb .type-badge { line-height: normal; }
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
      <span>&#128274; Secure • Verified Notes</span>
    </div>
  </div>

  <header class="site">
    <div class="container navbar">
      <a href="{{ url_for('index') }}" class="brand">
        <img src="{{ url_for('static', filename='aw-logo.png') }}" alt="{{ SITE_NAME }}" style="width:46px;height:46px;border-radius:12px;object-fit:cover;background:#6c2bd9;" onerror="this.onerror=null;this.src='data:image/png;base64,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';">
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

  <!-- PYQs SECTION -->
  <div class="optional-section">
    <a class="optional-toggle" href="{{ url_for('subject_page', slug='pyqs') }}" style="text-decoration:none;display:block;">
      <span class="opt-emoji">📝</span>
      <span>Previous Year Questions (PYQs)</span>
      <span class="opt-hint">🎯 Prelims + Mains PYQs — Click karke dekhein</span>
    </a>
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
<style>
  /* Mobile par preview clean rakho: topics list content ke NICHE, non-sticky */
  .preview-topics { position: sticky; top: 90px; max-height: 80vh; overflow: auto; }
  @media (max-width: 860px) {
    .detail-wrap { display: flex; flex-direction: column; }
    .detail-wrap .detail-main { order: 1; }
    .detail-wrap .preview-topics { order: 2; position: static; max-height: none; overflow: visible; margin-top: 24px; }
    .preview-topics ol { padding-left: 20px; }
    iframe { min-height: 480px !important; }
  }
</style>
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
    <div class="card preview-topics">
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
