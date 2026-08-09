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
      <a href="{{ url_for('note_view', note_id=n.id) }}" class="btn btn-ghost" target="_blank">👁️ View</a>
      <a href="{{ url_for('buy_note', note_id=n.id) }}" class="btn btn-primary">🛒 Buy</a>
    </div>
  </div>
</div>
""",
    'about.html': """{% extends "base.html" %}
{% block title %}About — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title"><h2>About Us</h2></div>
  <div class="card" style="max-width:820px;">
    <p><b>{{ SITE_NAME }}</b> ek platform hai jahan UPSC, BPCS aur State PCS aspirants ke liye premium, curated notes available hain.</p>
    <p>Hum cover karte hain:</p>
    <ul style="line-height:2;">
      <li>🌍 Geography</li>
      <li>🏛️ Polity</li>
      <li>📈 Economics</li>
      <li>🔬 Science &amp; Technology</li>
      <li>🏺 History</li>
      <li>🌿 Environment &amp; Ecology</li>
      <li>🎭 Art &amp; Culture</li>
      <li>📰 Current Affairs</li>
      <li>aur aur bhi... 🎯</li>
    </ul>
    <p style="color:var(--muted);">Har note expert teachers aur toppers se taiyar kiya gaya hai, clear aur concise language mein.</p>
  </div>
</div>
{% endblock %}
""",
    'admin_dashboard.html': """{% extends "base.html" %}
{% block title %}Admin Dashboard — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>🧑‍💼 Admin Dashboard</h2>
    <p>Notes manage karein — upload, featured, delete.</p>
  </div>

  <div class="stat-grid">
    <div class="stat"><div class="num">{{ total_notes }}</div><div class="lbl">Total Notes</div></div>
    <div class="stat"><div class="num">{{ total_files }}</div><div class="lbl">Files on Server</div></div>
    <div class="stat"><div class="num">{{ counts|length }}</div><div class="lbl">Subjects</div></div>
  </div>

  <div class="toolbar">
    <a href="{{ url_for('admin_upload') }}" class="btn btn-primary">➕ Naya Note Upload</a>
    <a href="{{ url_for('admin_subjects') }}" class="btn btn-ghost">🗂️ Manage Subjects</a>
    <a href="{{ url_for('index') }}" class="btn btn-ghost" style="margin-left:auto;">View Site →</a>
  </div>

  <!-- Subjects overview -->
  <h3 style="margin-top:30px;">Subjects Overview</h3>
  <div class="subject-grid" style="margin-bottom:30px;">
    {% for c in counts %}
      <a class="subject-card" href="{{ url_for('subject_page', slug=c.slug) }}">
        <div class="emoji">{{ subject_emoji(c.slug) }}</div>
        <div class="name">{{ c.name }}</div>
        <div class="count">{{ c.cnt }} notes</div>
      </a>
    {% endfor %}
  </div>

  <h3>Saare Notes ({{ notes|length }})</h3>
  <table class="admin-table">
    <thead>
      <tr>
        <th>ID</th><th>Title</th><th>Subject</th><th>Type</th><th>Price</th><th>Featured</th><th style="width:190px;">Actions</th>
      </tr>
    </thead>
    <tbody>
      {% for n in notes %}
      <tr>
        <td>#{{ n.id }}</td>
        <td><a href="{{ url_for('note_detail', note_id=n.id) }}"><b>{{ n.title }}</b></a></td>
        <td>{{ subject_name(n.subject_slug) }}</td>
        <td><span class="type-badge" style="position:static;background:var(--primary);">{{ n.file_type }}</span></td>
        <td>₹{{ '%g' % n.price }}</td>
        <td>
          <form method="post" action="{{ url_for('admin_toggle', note_id=n.id) }}">
            <button class="btn btn-sm {{ 'btn-warn' if n.featured else 'btn-ghost' }}">
              {{ '⭐ Featured' if n.featured else '☆ Feature' }}
            </button>
          </form>
        </td>
        <td>
          <a href="{{ url_for('note_detail', note_id=n.id) }}" class="btn btn-sm btn-ghost">View</a>
          <form method="post" action="{{ url_for('admin_delete', note_id=n.id) }}" style="display:inline;"
                onsubmit="return confirm('Confirm: \\'{{ n.title }}\\' delete karein?');">
            <button class="btn btn-sm btn-danger">🗑️</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="7" style="text-align:center; padding:30px;">Abhi koi notes nahi hain. <a href="{{ url_for('admin_upload') }}">Pehla note upload karein →</a></td></tr>
      {% endfor %}
    </tbody>
  </table>
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
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}?v=8-premium">
  <!-- Critical CSS: CSS load hone se pehle bhi layout sahi rahe (no flicker) -->
  <style>
    html, body { margin: 0; padding: 0; }
    *, *::before, *::after { box-sizing: border-box; }
    body { font-family: 'Segoe UI', -apple-system, 'Georgia', 'Roboto', system-ui, sans-serif; background: #faf7f1; }
    .container { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
    .hero { background: linear-gradient(135deg, #0c5c3a, #073c25, #052a1a); padding: 60px 0 70px; text-align: center; }
    .hero h1 { margin: 22px 0 14px; font-size: 44px; line-height: 1.1; }
    .navbar { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; padding: 14px 0; }
  </style>
</head>
<body>

  <div class="topbar">
    <div class="container">
      <span>✦ UPSC | BPSC | State PCS — Premium Notes</span>
      <span>{% if is_admin %}<a href="{{ url_for('admin_dashboard') }}">🧑‍💼 Admin Panel</a>{% else %}<a href="{{ url_for('admin_login') }}">Admin Login</a>{% endif %}</span>
    </div>
  </div>

  <header class="site">
    <div class="container navbar">
      <a href="{{ url_for('index') }}" class="brand">
        <div class="brand-logo">U</div>
        <div>
          <div class="brand-name">UPSC<span>Notes</span></div>
          <div class="brand-tag">{{ SITE_TAGLINE }}</div>
        </div>
      </a>

      <form class="searchbar" action="{{ url_for('browse') }}" method="GET">
        <input type="text" name="q" placeholder="Search premium notes..." value="{{ request.args.get('q','') }}">
        <button type="submit">🔍</button>
      </form>

      <nav class="nav-links">
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('browse') }}">All Notes</a>
        <a href="{{ url_for('about') }}">About</a>
        <a href="{{ url_for('contact') }}">Contact</a>
        {% if is_admin %}
          <a class="admin-btn" href="{{ url_for('admin_upload') }}">+ Upload</a>
          <a class="admin-btn" href="{{ url_for('admin_logout') }}">Logout</a>
        {% else %}
          <a class="admin-btn" href="{{ url_for('admin_login') }}">Admin</a>
        {% endif %}
        <button class="theme-toggle" id="themeToggle" title="Dark/Light">🌙</button>
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
          <a href="{{ url_for('browse') }}">All Notes</a>
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
      <div class="copy">© {{ now_year() }} {{ SITE_NAME }} — Sabhi adhikaar surakshit.</div>
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
      <a class="subject-card" href="{{ url_for('subject_page', slug=s.slug) }}">
        <span class="emoji">{{ subject_emoji(s.slug) }}</span>
        <span class="name">{{ s.name }}</span>
        <span class="count">{{ s.hindi }} · {{ s.cnt }} notes</span>
      </a>
    {% endfor %}
  </div>

  <!-- Features -->
  <div class="feature-grid">
    <div class="feature-card"><div class="ico">📄</div><h3>PDF & HTML</h3><p>Easy to read &amp; print</p></div>
    <div class="feature-card"><div class="ico">🎯</div><h3>Exam-Focused</h3><p>Prelims + Mains</p></div>
    <div class="feature-card"><div class="ico">💳</div><h3>Secure UPI</h3><p>QR scan karke</p></div>
    <div class="feature-card"><div class="ico">⚡</div><h3>Instant Access</h3><p>Turant delivery</p></div>
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

  <!-- Recent -->
  <div class="section-title">
    <div class="tag">Fresh</div>
    <h2>Recently <em>Added</em></h2>
    <p>Sabse nayi uploads.</p>
  </div>
  <div class="note-grid">
    {% for n in recent %}
      {% include "_note_card.html" %}
    {% endfor %}
  </div>

  <!-- CTA -->
  <div class="cta-banner">
    <h2>Unlock Your Full Potential</h2>
    <p>Complete bundles mein saare notes ek saath — better price, better preparation.</p>
    <a href="{{ url_for('browse') }}" class="btn btn-gold">🛒 Start Learning Now</a>
  </div>

  {% if not recent %}
    <div class="card" style="text-align:center; padding:40px;">
      <div style="font-size:50px;">📭</div>
      <h3>Abhi koi notes nahi hain</h3>
      <p>Admin abhi notes upload karega.</p>
      {% if is_admin %}
        <a href="{{ url_for('admin_upload') }}" class="btn btn-green">+ Pehla Note Upload Karein</a>
      {% endif %}
    </div>
  {% endif %}

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
        <a href="{{ url_for('note_view', note_id=note.id) }}" class="btn btn-ghost" target="_blank">👁️ Preview</a>
        <a href="{{ url_for('download_note', note_id=note.id) }}" class="btn btn-outline" style="border-color:var(--primary);color:var(--primary);">⬇️ Download</a>
        {% if is_admin %}
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
    'subject.html': """{% extends "base.html" %}
{% block title %}{{ subject.name }} Notes — {{ SITE_NAME }}{% endblock %}

{% block content %}
<div class="container">
  <div class="section-title">
    <h2>{{ subject_emoji(subject.slug) }} {{ subject.name }} Notes <span style="font-size:16px;color:var(--muted);font-weight:400">({{ subject.hindi }})</span></h2>
    <p>{{ notes|length }} notes is subject mein available.</p>
  </div>

  {% if notes %}
    <div class="note-grid">
      {% for n in notes %}
        {% include "_note_card.html" %}
      {% endfor %}
    </div>
  {% else %}
    <div class="card" style="text-align:center; padding:50px;">
      <div style="font-size:50px;">📭</div>
      <h3>Is subject mein abhi notes nahi hain</h3>
      <p>Jald hi aayenge. Tab tak doosre subjects check karein.</p>
      <a href="{{ url_for('browse') }}" class="btn btn-primary">All Notes</a>
    </div>
  {% endif %}
</div>
{% endblock %}
""",
}
