# 📚 UPSC Notes Store

Ek simple website jahan aap **UPSC/State PCS ke paid notes bech sakte hain**.
Admin (aap) **PDF aur HTML files upload aur delete** kar sakte hain, notes ko **featured** bana sakte hain, aur **subjects** manage kar sakte hain.

> **Payment:** Manual / UPI QR — buyer aapko WhatsApp/Call/Email se contact karke payment karta hai. (Koi payment gateway nahi lagana pada.)

---

## ✨ Features

- **Storefront (public)** — sab notes, subjects ke hisaab se, search + filter + sort ke saath
- **Sab UPSC subjects** — Geography, Polity, Economics, History, Science & Tech, Environment, Art & Culture, Current Affairs, Ethics, IR, CSAT, Prelims, Mains + aur add kar sakte hain
- **PDF aur HTML notes** upload karein (up to 100 MB)
- **Admin Panel** — ek login se upload, delete, featured toggle, subjects manage
- **Buy page** — price + UPI QR scan, WhatsApp/Call/Email se payment
- **Hinglish UI** — Hindi-English mix

---

## 🚀 Kaise Chalayein (Local)

```bash
cd upsc-notes-store
pip install -r requirements.txt
python app.py
```

Browser mein kholen: **http://127.0.0.1:5000**

- Storefront: `http://127.0.0.1:5000`
- Admin login: `http://127.0.0.1:5000/admin/login`

### 🔑 Default Admin Login
| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `aj521900` |

> 💡 Password aapne apni details se set kar li hai. Badalni ho to `app.py` ke sabse upar `ADMIN_PASSWORD` badlein.

---

## ⚙️ Apni Settings Badlein (`app.py` ke top par)

```python
SITE_NAME       = "UPSC Notes Store"          # Site ka naam
SITE_TAGLINE    = "Premium UPSC Notes..."     # Tagline
ADMIN_USERNAME  = "admin"                     # Admin username
ADMIN_PASSWORD  = "aj521900"                  # Aapka password
SESSION_SECRET  = "..."                       # Security key
UPI_ID          = "9569431430@ybl"            # Apna UPI ID
SELLER_PHONE    = "+91-9569431430"            # Aapka phone
SELLER_WHATSAPP = "+919569431430"             # Aapka WhatsApp
SELLER_EMAIL    = "as5093220@gmail.com"       # Aapka email
```

### 📲 UPI QR Code Add Karein
1. UPI QR ke liye ye command chalayein (apne UPI ID ke saath):
   ```bash
   pip install qrcode Pillow
   python make_qr.py "yourname@upi"
   ```
   Isse `uploads/upi/qr.png` ban jayega — buy page par automatically dikhega.
2. Ya phir apna koi bhi QR image naam se rakh dein:
   `uploads/upi/qr.png`

---

## 🖥️ Kaise Use Karein

### Naya Note Upload Karna
1. `/admin/login` par login karein
2. **"+ Upload"** button dabayein (ya Dashboard → Naya Note Upload)
3. Bharein: **Title, Subject, Description, Price**, aur **PDF/HTML file**
4. **Upload Karin** — note storefront par dikh jayega

### Note Delete Karna
1. Dashboard mein note ke aage **🗑️** button dabayein
2. Confirm karein — file aur database record dono delete ho jayenge

### Subject Add/Delete
1. Dashboard → **Manage Subjects**
2. Naya subject add karein ya purana delete karein

---

## 📁 Project Structure

```
upsc-notes-store/
├── app.py                  # Main Flask application + settings
├── make_qr.py              # UPI QR generator
├── seed_demo.py            # Demo notes add karne ke liye (optional)
├── requirements.txt        # Python dependencies
├── upsc.db                 # SQLite database (auto-banti hai)
├── static/
│   └── style.css           # Stylesheet
├── templates/              # HTML templates
│   ├── base.html           # Layout (header/footer/nav)
│   ├── index.html          # Home page
│   ├── browse.html         # All notes + search/filter
│   ├── subject.html        # Subject page
│   ├── note_detail.html    # Single note page
│   ├── buy.html            # Payment/buy page
│   ├── admin_*.html        # Admin pages
│   └── ...
└── uploads/
    ├── pdfs/               # Uploaded PDF files
    ├── html/               # Uploaded HTML files
    └── upi/qr.png          # UPI QR code
```

---

## 🚢 Online Deploy Karna (Real Website)

Isse **free hosting** par daal sakte hain:

### Option A — Render.com (recommended, free)
1. Code GitHub par push karein
2. [render.com](https://render.com) → **New Web Service** → GitHub repo link karein
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy — aapko ek **live URL** milega (jaise `https://yourstore.onrender.com`)

### Option B — PythonAnywhere (free)
1. [pythonanywhere.com](https://pythonanywhere.com) par account banayein
2. Files upload karein, `requirements.txt` install karein
3. WSGI mein `app` import karein

> 💡 **Note:** Deploy karne se pehle **`ADMIN_PASSWORD` aur `SESSION_SECRET`** zaroor badlein.

---

## 🔒 Security Notes
- File uploads sirf **PDF/HTML** allow hote hain (dusri files reject)
- Files ko unique naam se store kiya jata hai
- Admin pages par login required hota hai
- Files `uploads/` folder ke andar rakhin, kisi bhi sensitive data (jaise admin details) ko `uploads/` mein na rakhin
