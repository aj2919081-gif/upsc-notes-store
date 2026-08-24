# 📚 UPSC Notes Store

Ek simple website jahan aap **UPSC/State PCS ke paid notes bech sakte hain**.
Admin (aap) **PDF aur HTML files upload aur delete** kar sakte hain, notes ko **featured**
bana sakte hain, aur **subjects** manage kar sakte hain.

> **Payment:** Manual UPI QR + Razorpay — buyer UPI QR scan karke ya Razorpay se
> pay karta hai, purchase account mein save hota hai.

---

## ✨ Features

- **Storefront (public)** — sab notes, subjects ke hisaab se, search + filter + sort
- **Sab UPSC subjects** — Geography, Polity, Economics, History, Science & Tech,
  Environment, Art & Culture, Current Affairs, Ethics, IR, CSAT, Prelims, Mains + aur
- **HTML notes** (DB mein stored) + PDF support (100 MB max)
- **Admin Panel** — login ke saath upload, delete, featured toggle, subjects manage
- **Buy page** — price + UPI QR / Razorpay checkout
- **User accounts** — buyers ke purchases account mein save, library page se access
- **Hinglish UI**

---

## 🚀 Kaise Chalayein (Local)

Pehle environment variables set karo (ye **zaroori** hain — app inke bina start nahi hoti):

```bash
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="apna-strong-password-123"
export ADMIN_TOKEN="apna-secret-url-token"        # jaise: /apna-token/login
export SESSION_SECRET="random-48-chars-secret"     # python3 -c "import secrets; print(secrets.token_urlsafe(48))"
export SESSION_COOKIE_INSECURE=1                  # sirf local HTTP testing ke liye
# optional:
export UPI_ID="apna@upi"
export SELLER_PHONE="+91-XXXXXXXXXX"
export SELLER_WHATSAPP="+91XXXXXXXXXX"
export SELLER_EMAIL="you@example.com"
export RAZORPAY_KEY_ID="rzp_test_xxx"
export RAZORPAY_KEY_SECRET="xxx"
```

Phir:

```bash
pip install -r requirements.txt
python app.py
```

- Storefront: `http://127.0.0.1:5000`
- Admin login: `http://127.0.0.1:5000/<ADMIN_TOKEN>/login`

> ⚠️ **Secrets kabhi code ya repo mein hardcode NAHI karein.** Purani hardcoded
> values (admin password, admin token, Razorpay key) public repo mein chali gayi
> thi — isliye 24 Aug 2026 ko sab rotate kar diya gaya. Nayi values sirf env vars
> (Render Dashboard) mein rakhein.

---

## 🖥️ Kaise Use Karein

1. `/admin/login` (secret token URL) par login karein
2. **"+ Upload"** — Title, Subject, Description, Price + file
3. Dashboard se delete / featured toggle / subjects manage
4. Manual UPI payment aayi toh **Purchase** page se customer ko bundle access dein
   (Razorpay payment khud-grant hota hai)

### 📲 UPI QR Code

```bash
pip install qrcode Pillow
python make_qr.py "apna@upi"     # uploads/upi/qr.png banata hai
```
Ya embedded QR update karne ke liye `make_qr.py` + `_qr_embed.py` regenerate karein.

---

## 📁 Project Structure (ACTUAL)

```
upsc-notes-store/
├── app.py                  # Main Flask app (saare routes + settings)
├── _embedded_templates.py  # Saare HTML templates (Python module mein embedded)
├── _qr_embed.py            # UPI QR (base64)
├── make_qr.py              # Naya UPI QR banane ke liye
├── seed_demo.py            # Demo notes (optional)
├── make_bundle*.py, upload_ancient.py  # One-off migration scripts
├── upsc.db                 # SEED database (413 notes, PII-free) — content isme hi hai
├── requirements.txt        # Pinned (tested) versions
├── render.yaml             # Render.com deploy blueprint (env vars se secrets)
├── REVIEW.md               # Full code review + security report
├── tools/                  # One-off migration scripts (batch upload ke liye)
├── static/                 # PWA icons
└── uploads/                # Runtime uploads (empty structure; files ephemeral hain)
    ├── pdfs/
    ├── html/
    └── upi/
```

> **Note:** `templates/` aur `static/style.css` folders NHI hain — templates
> `_embedded_templates.py` mein hain, CSS `base.html` template ke andar inline hai.

---

## 🚢 Online Deploy (Render.com)

1. GitHub par push karein
2. [render.com](render.com) → **New → Blueprint** → ye repo select karein
   (ya Web Service bana ke env vars manually set karein)
3. `render.yaml` mein `generateValue: true` wale secrets Render Dashboard se
   dekhein: **ADMIN_PASSWORD** aur **ADMIN_TOKEN** ki values Dashboard →
   Environment Variables mein hain — admin URL `https://site/<ADMIN_TOKEN>/login`
4. **Razorpay keys** Dashboard mein manually add karein (na karein toh sirf
   manual UPI payment chalega — site band nahi hogi)

### ⚠️ Data Persistence (important)

Render free tier ka filesystem **ephemeral** hai — har deploy/restart par
`uploads/` aur DB ke naye writes reset ho jate hain:
- Repo mein wala `upsc.db` sirf **seed** hai (notes + subjects, PII se sanitized)
- Naye user accounts / Razorpay purchases deploy ke baad **reset** ho jate hain
- **Backup zaroor banayein**: rozana DB ka backup (Render se DB download karna
  aaj ke liye possible nahi hai free tier par — isliye purchases ko
  offsite track karein, jaise Google Sheet)
- Purani details: `REVIEW.md` mein issue H1

---

## 🔒 Security (24 Aug 2026 hardening)

- [x] Secrets sirf env vars se — code/repo mein kuch bhi nahi; startup par
      missing secret se app start nahi hoti
- [x] Admin token ab `/manifest.json` / `/service-worker.js` se leak nahi hota
      (wo admin prefix ke neeche + login ke saath)
- [x] CSRF protection (session token, saare POST forms) + `SameSite=Lax` cookies
- [x] Open-redirect fix (`next` param sirf same-site paths)
- [x] Security headers: CSP, nosniff, X-Frame-Options, Referrer-Policy, HSTS
- [x] Razorpay verify: note_id client-side se NAHI — Razorpay order ke notes se;
      amount + status + replay check
- [x] Login brute-force throttle (5 tries / 5 min)
- [x] `debug=False`
- [ ] **Aapko karna hai:** purani values (jo repo history mein hain) Render par
      set kiye gayi hui hain toh rotate karein; Razorpay ke **test keys bhi public
      the** — Razorpay dashboard se naye keys generate karein
- [ ] **Aapko karna hai:** repo ki purani history (jisme purana DB + secrets the)
      delete/recreate karke clean repo push karein — `SETUP.md` mein steps

Purani issues ki list: `REVIEW.md`
