# 📋 UPSC Notes Store — Full Website Review

**Date:** 24 Aug 2026 · **Repo:** github.com/aj2919081-gif/upsc-notes-store · **Commit reviewed:** `784ac48`

## 1. Overview

| Kya hai | Detail |
|---|---|
| Stack | Flask (single `app.py`, 1340 lines) + SQLite + embedded Jinja templates (`_embedded_templates.py`, 112 KB) |
| Content | 413 notes (411 HTML + 2 PDF) — **poora content `upsc.db` mein gzip-compressed** hai, `uploads/` folder repo mein nahi hai |
| Payment | Manual UPI QR + Razorpay (**abhi Test mode** — live key lagana hoga) |
| Admin | Secret-URL panel (`/aj-secret-admin-XXXX (dead)/...`) + PWA manifest/service-worker |
| Deploy | Render.com (free tier) — `render.yaml` + `Procfile` (dono, duplicate) |

App local par sahi se start hota hai, storefront render hoti hai, Razorpay ka secret key client par nahi jaata (verified ✅).

---

## 2. 🔴 CRITICAL — aaj hi theek karein

### C1. "Secret" admin URL publicly exposed hai (VERIFIED) — ✅ FIXED (24 Aug 2026)
`/manifest.json` aur `/service-worker.js` public routes par the aur dono mein admin token hardcode tha:

```json
"start_url": "/aj-secret-admin-XXXX (dead)/"
```
**Applied fix:** Manifest + service-worker ab `ADMIN_PREFIX` ke neeche hain (`/<token>/manifest.json`, `/<token>/service-worker.js`) aur dono par `@login_required` hai. Root par ab 404. Admin template `url_for()` use karte hain isliye references auto-update ho gaye. **Token rotate bhi kiya** (purana git history mein hai) — nayi value `SETUP.md` mein. Verified: root 404, no-auth 302→login, logged-in 200.

### C2. Secrets + personal data public repo mein committed — ✅ CODE/REPO SIDE FIXED (24 Aug 2026)
Purani values: admin password `aj52XXXX (dead)`, admin token `aj-secret-admin-XXXX (dead)`, Razorpay key **secret** (test), weak `SESSION_SECRET`, UPI/phone/email.

**Applied fix:**
- `app.py` se saare hardcoded secrets hataaye — ab **env vars se hi** aate hain; missing secret par app **start hi nahi hoti** (fail-fast, verified)
- `render.yaml`: `generateValue: true` (SESSION_SECRET, ADMIN_PASSWORD, ADMIN_TOKEN); Razorpay keys ke liye dashboard-instructions (generate nahi ho sakti); sirf public business info values ke roop mein rahi
- `README.md`: saare asli secrets/personal data hata ke placeholders + env-var instructions
- **Nayi strong values generate ki hain** — `SETUP.md` mein (wo file `.gitignore` mein hai, commit nahi hogi)
- **Aapko karna hai:** GitHub repo delete+recreate karke clean repo push karein (history saaf ho jayegi — `SETUP.md` mein step-by-step) aur Razorpay dashboard se naye keys lein (purane test keys public the)

### C3. 23 MB `upsc.db` git mein hai — real user data public — ✅ SANITIZED (24 Aug 2026)
DB mein 9-10 users (asli Gmail shamil), purchase records the.

**Applied fix:** DB se `users`, `payments`, `purchases` tables poora wipe (PII gone); 413 notes + 28 subjects (public content) intact. Repo mein wala DB ab **PII-free seed data** hai — commit rakhna acceptable hai. `.gitignore` mein runtime uploads ignore (sirf folder structure tracked).
**Note:** Render ephemeral-FS issue alag hai (H1) — naye runtime purchases deploy par reset hote hain; backup strategy zaroori hai.

### C4. Razorpay verify mein note/amount mismatch (direct money leak) — ✅ FIXED (24 Aug 2026)
`/pay/verify` form se aaya **client-side `note_id`** par bharosa karta tha — sirf payment signature verify hota hai, ye nahi check kiya jata ki paid order wahi note ka tha jiska id bheja gaya.
Matlab: ₹49 wali world-history bundle par payment karke, verify form mein ₹499 geography bundle ka `note_id` bhej diya → poora meha bundle free.

**Applied fix (`app.py` mein, tested):**
- `pay_order` ab order ke `notes` field mein `{"note_id": ..., "amount_paise": ...}` store karta hai — ye Razorpay ke server-side rehta hai, client change nahi kar sakta.
- `pay_verify` ab form wala `note_id` **poora ignore** karta hai; note_id sirf Razorpay se fetch kiye gaye order ke `notes` se aata hai.
- Verify chain: (1) HMAC signature → (2) order fetch + `status == "paid"` + `payment_id` sanity → (3) `order.amount == order-time recorded amount` (legacy orders ke liye note ki current price) → (4) replay protection: same `payment_id` dobara process nahi hota, purchase insert idempotent (double grant nahi hota).
- Free/₹0 notes par `/pay/<id>` ab direct view/download par redirect karta hai (order hi nahi banta).
- **Verified end-to-end:** test order `order_TTfNR6kc5RPzXG` banaya, Razorpay API se fetch karke confirm kiya ki `notes: {"note_id": "407", "amount_paise": "4900"}` store hai. Fake signature POSTs par bhi clean 302 (koi 500 nahi).

### C5. Open redirect (VERIFIED) — ✅ FIXED (24 Aug 2026)
```
POST /signup?next=https://evil.example.com/phish  →  302 https://evil.example.com/phish
```
**Applied fix:** `safe_next()` helper — sirf same-site relative paths (`/...`, bina scheme/netloc/`//`) allow hote hain; baaki sab fallback par. `/login`, `/signup`, `admin_login` — teeno par laga. Verified: `next=https://evil.com` ab `302 /` (fallback) deta hai.

### C6. No CSRF protection (koi token nahi, cookie flags bhi weak) — ✅ FIXED (24 Aug 2026)
**Applied fix:**
- Session-based CSRF token (`secrets.token_urlsafe(32)`) — context processor se har template mein `{{ csrf_token }}`, aur `before_request` mein har POST/PUT/DELETE/PATCH par `secrets.compare_digest` check. Token na ho → **403** (friendly page ke saath).
- Saare 9 POST forms mein hidden input add (admin login/upload/delete/toggle/subjects/purchase + user login/signup) + Razorpay JS form mein bhi token field.
- `SESSION_COOKIE_SAMESITE = "Lax"` + `SESSION_COOKIE_SECURE` (HTTPS deploy par auto; local testing ke liye `SESSION_COOKIE_INSECURE=1`).
Verified: bina token POST → 403; token ke saath login flow → 302 dashboard.

### C7. Stored XSS via HTML notes — ✅ FIXED (24 Aug 2026)
Upload kiye gaye HTML notes pehle `text/html` ke roop mein **as-is serve** hote the (`clean_note_html()` sirf `@import`/`@font-face` hataata tha — `<script>` aur `on*` handlers nahi).

**Applied fix (3 layers):**
1. `/note/<id>/view` ab **wrapper page** render karta hai — upar sticky bar (Wapas / title / Download) + neeche `<iframe sandbox="allow-same-origin" src="/note/<id>/view/content">`. `sandbox` ke bina `allow-scripts` = **note ka koi bhi script/on* handler execute nahi hota**.
2. Naya route `/note/<id>/view/content` raw note HTML serve karta hai (same access checks: free/demo/purchased/admin) — sirf sandboxed iframe ke liye.
3. Us path par CSP `script-src 'none'` (double cover) + bundle preview (`preview.html`) ke dono iframes par bhi `sandbox` lagaya.
- **Bonus UX:** pehle note ke andar koi back button nahi tha (user site se "bahar" feel karta tha) — ab wrapper se Wapas/Download hamesha visible.
- **Trade-off:** notes mein agar legitimate interactive JS hota (quizzes etc.) wo ab nahi chalega — notes store ke liye sahi call.
Verified: wrapper 200 + sandboxed iframe, content route 200 + `script-src 'none'`, paid note bina purchase → buy redirect (dono routes par).

---

## 3. 🟠 HIGH

### H1. Render free tier = ephemeral filesystem (data loss risk)
Free instance par har deploy/restart par local FS reset hota hai. Aapka workaround (DB git commit karna) chalta hai, lekin:
- Deploy ke baad hui **nayi purchases/uploads silently delete** ho jate hain,
- 100 MB PDF uploads ke baad next deploy par gayab.
**Fix:** Render paid persistent disk, ya better: external DB (Supabase/Neon/SQLite on R2) + files S3/R2 par. Kam se kam: har din DB ka backup script.

### H2. Admin login: weak, unhashed, no rate-limit — ✅ PARTIALLY FIXED (24 Aug 2026)
- ✅ **Throttling:** login (user + admin) par in-memory brute-force throttle — 5 galat koshishen / 5 min (admin: 600s window), successful login par reset. (In-memory hai, har gunicorn worker apna count rakhta hai — is scale par kaafi.)
- ✅ **Timing-safe compare:** `secrets.compare_digest()` (plaintext `==` ki jagah).
- ✅ **Strong password:** 22-char random value `SETUP.md` mein; ab env-var se aata hai, koi weak default nahi.
- ⬜ *Optional future:* admin password ko hash store karna (env-var plaintext chhoti app ke liye acceptable hai).

### H3. `debug=True` in `app.run()` — ✅ FIXED
`debug=False` ho gaya (Werkzeug debugger RCE risk gone). Production par gunicorn hi chalta hai.

### H4. Zero security headers — ✅ FIXED
Ab har response par: `Content-Security-Policy` (Razorpay CDN + inline ke liye tuned), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`. Verified via curl.

### H5. PWA icons broken (VERIFIED) — ✅ FIXED
`static/aw-logo-192.png` + `aw-logo-512.png` generate karke repo mein daal diye — ab dono 200 dete hain, admin PWA install ho payega.

---

## 4. 🟡 MEDIUM

| # | Issue | Status (24 Aug 2026) |
|---|---|---|
| M1 | Documentation drift (README galat structure batata tha) | ✅ FIXED — README ko actual structure se sync kiya (embedded templates, inline CSS, tools/, static/) |
| M2 | `temp.txt` (1 byte junk) | ✅ FIXED — delete |
| M3 | One-off scripts mein absolute paths (`/home/user/...`) | ✅ FIXED — scripts `tools/` folder mein move + paths `__file__`-relative |
| M4 | `DEMO_PREVIEW_IDS` import-time (stale) | ✅ FIXED — 60s TTL cache wala `demo_preview_ids()` function |
| M5 | N+1 queries (index per-subject bundle) + per-request `get_subjects()` | ✅ FIXED — bundles single query; subjects 60s TTL cache (admin change par invalidate) |
| M6 | SQLite WAL/indexes missing | ✅ FIXED — `journal_mode=WAL`, `busy_timeout=5000`, 5 indexes (verified) |
| M7 | `admin_toggle` referrer redirect | ✅ FIXED — hamesha dashboard par wapas |
| M8 | Min password 4 chars + no audit trail | ✅ FIXED (partial) — min 8 chars (verified: 5-char reject), `admin_actions` audit table + purchase grants log. Email verification future mein |
| M9 | `requirements.txt` unpinned | ✅ FIXED — tested versions pinned (flask 3.1.3, razorpay 2.0.1, etc.) |
| M10 | `Procfile` + `render.yaml` dono | ⬜ Decision: dono rakhe (Procfile 1-line hai, harmless — Heroku fallback ke liye); README mein Render primary hai |
| M11 | Email mismatch (2 alag emails) | ⬜ Aapko sahi email set karni hai — SETUP.md mein flag lagaya |
| M12 | Sitemap: per-request query + fake lastmod | ✅ FIXED — 1-hour cache + asli lastmod (`created_at`) (verified: 08-08/08-10/08-11... dates) |
| M13 | Kuch subjects (ethics, IR, CSAT, CA) ke liye "Complete Bundle" missing — content gap | ⬜ Content work (aapka): in subjects ke bundles banayein, ya storefront par "coming soon" state |

---

## 5. 🟢 Kya Kya Sahi Hai (keep doing)

- **Saara SQL parameterized** — koi injection nahi mili ✅
- Uploads ko **UUID naam** se store kiya, `send_from_directory` sahi use — path traversal safe ✅
- User passwords **hashed** (werkzeug) ✅
- Razorpay **key secret client par nahi jaata** (pay page verified) ✅
- SEO basics solid: title/meta/OG tags, `robots.txt`, `sitemap.xml`, Google site-verification ✅
- Hinglish UX consistent, note rendering ke liye mobile-responsive CSS inject karna smart fix hai ✅
- 413 notes ka content DB mein compressed store karna — Render ephemeral-FS problem ka practical workaround hai (data-loss risk ke saath, dekho H1) ✅
- Pricing clean: 12 bundles, ₹49–₹499, original_price discount display ke saath ✅

---

## 6. ✅ Priority Action List (order of work)

1. ~~**Aaj:** Saari secrets rotate karein~~ — ✅ DONE: code se hataaye + nayi values `SETUP.md` mein. **Aapko:** Render Dashboard mein set karna + Razorpay keys regenerate karna.
2. ✅ **DONE:** `/manifest.json` + `/service-worker.js` se admin token leak fix (C1) — verified.
3. ✅ **DONE:** `upsc.db` sanitized (PII gone), `.gitignore` update (C3). **Aapko:** repo delete+recreate karke clean history push karna (SETUP.md Step 1).
4. ✅ **DONE (24 Aug):** Razorpay verify mein order↔note↔amount matching (C4) — fixed + tested.
5. ✅ **DONE:** CSRF + cookie flags (C6), open-redirect fix (C5) — verified.
6. ✅ **DONE (C7):** HTML notes ab sandboxed iframe wrapper ke through — stored-XSS fixed (3 layers).
7. ✅ **DONE:** Login throttling (H2 partial), `debug=False` (H3), security headers (H4).
8. ✅ **DONE:** M-series cleanup (M1–M6, M8, M9, M12) — details upar M-table mein; `tools/` folder, pinned requirements, WAL+indexes, TTL caches, audit table.
9. ⬜ **Next:** Persistent storage ka plan (H1) — naye purchases/users deploy par reset hote hain; backup routine banayein.
10. ⬜ **Aapke paas:** Repo reset (SETUP.md Step 1), Render env vars (Step 2), Razorpay keys (Step 3), M11 email verify, M13 bundles content.

---

## 7. 🔧 24 Aug 2026 Session — Kya Kya Fixed Hota Hai (verified)

| # | Fix | Status |
|---|---|---|
| 1 | Razorpay verify: note_id client-side se hata, order `notes` se + amount/status/replay checks (C4) | ✅ tested end-to-end |
| 2 | Manifest + service-worker admin prefix ke neeche + login (C1) | ✅ verified 404/302/200 |
| 3 | Saare secrets env-var only + fail-fast startup check (C2 code side) | ✅ verified (bina secret app band) |
| 4 | DB sanitized — users/payments/purchases wipe, content intact (C3) | ✅ |
| 5 | Open-redirect fix — `safe_next()` login/signup/admin_login (C5) | ✅ verified |
| 6 | CSRF protection — saare 9 POST forms + Razorpay JS form + SameSite=Lax (C6) | ✅ verified 403/302 |
| 7 | Security headers — CSP, nosniff, XFO, Referrer-Policy, HSTS, Permissions-Policy (H4) | ✅ verified |
| 8 | Login brute-force throttle (user 5/5min, admin 5/10min) + timing-safe admin compare (H2) | ✅ |
| 9 | `debug=False` (H3) | ✅ |
| 10 | PWA icons generate — `static/aw-logo-192/512.png` (H5) | ✅ verified 200 |
| 11 | `admin_toggle` referrer redirect hataya (M7) | ✅ |
| 12 | **Bonus:** 2 "PDF" notes (PYQs 2011/2012) jo 404 de rahe the — content DB mein hi tha, `file_type='html'` karke fix — ab free download bhi chalta hai | ✅ verified |
| 13 | Trailing-slash dashboard route (minor UX) | ✅ |
| 14 | C7: Note view → sandboxed iframe wrapper + `/view/content` route (`script-src 'none'`) + preview iframes par `sandbox` — stored-XSS fixed, bonus: notes ke andar Wapas/Download bar | ✅ verified |
| 15 | M2: `temp.txt` delete | ✅ |
| 16 | M3: One-off scripts → `tools/` folder, hardcoded `/home/user/...` paths hataaye | ✅ |
| 17 | M4: `DEMO_PREVIEW_IDS` → 60s TTL cache (naye notes par stale nahi) | ✅ |
| 18 | M5: `index()` N+1 bundles → 1 query; `get_subjects()` 60s TTL cache + admin invalidate | ✅ |
| 19 | M6: SQLite WAL mode + `busy_timeout=5000` + 5 indexes | ✅ verified |
| 20 | M8: Signup min password 8 + `admin_actions` audit table (purchase grants logged) | ✅ verified (5-char reject) |
| 21 | M9: `requirements.txt` pinned (tested versions) | ✅ |
| 22 | M12: Sitemap 1h cache + asli lastmod | ✅ verified |
| 23 | Dead code: `bundle_preview_sample()` (unused, fragile regex) delete | ✅ |

**Abhi aapke paas baaqi (SETUP.md mein steps):**
1. GitHub repo delete + recreate + clean push (purani history se DB + secrets saaf honge)
2. Render Dashboard mein naye env vars set (ya blueprint auto-generate)
3. Razorpay dashboard se naye keys + dashboard mein set
4. Backup routine (H1)
5. Optional: C7 (note sandbox), M1–M10 cleanup

**Bottom line:** Product ka structure accha hai aur content library solid hai, lekin security foundation abhi public-internet ke liye ready nahi hai — esp. token leak (C1), committed secrets/DB (C2/C3) aur Razorpay mismatch (C4). In 4 ko fix karte hi site ka risk profile bahut better ho jayega.
