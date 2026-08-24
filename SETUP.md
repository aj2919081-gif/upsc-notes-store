# 🔑 SETUP — Naye Secrets + Clean Repo (24 Aug 2026)

> ⚠️ **Is file ko KABHI git/repo mein commit NAHI karna.**
> Isme naye secret values hain — sirf aapki setup ke liye hai.
> (Isliye `.gitignore` mein bhi add hai.)

## Kya hua?

Purani values public repo (aur git history) mein committed ho chuki thin:
- Admin password: `aj521900`
- Admin token: `aj-secret-admin-x7q9z2`
- Razorpay test key secret: `8gywbRTay4qslNVywyLWEp4L`
- 23 MB DB jisme 9 users ke emails the

**Isliye sab rotate kiye gaye hain — purani values hamesha ke liye dead hain.**

---

## Step 1 — GitHub repo ki history saaf karo (ZAROORI)

Code mein secrets hata diye gaye hain, lekin **git history** mein purana DB +
secrets abhi bhi hain. History saaf karne ka sabse aasaan tarika —
repo delete + recreate:

```bash
# 1. GitHub par: repo Settings → (bottom) Delete this repository
#    (repo ka naam type karke confirm karein)
# 2. Same naam se nayi repo banayein (EMPTY — koi README nahi)
# 3. Apne computer par:
cd upsc-notes-store          # ye folder jo aapne naya code zip se unpack kiya
git init -b main
git add -A
git commit -m "Clean start — secrets removed, security hardening applied (24 Aug 2026)"
git remote add origin https://github.com/aj2919081-gif/upsc-notes-store.git
git push -u origin main
```

> Zip mein jo `upsc-notes-store/` folder hai, usme pehle se clean
> `.git` history bhi ready hai (single commit) — sirf
> `git remote add` + `git push` karna hoga.

Push hote hi Render auto-deploy karega (agar repo linked hai; warna
Render par manually "trigger deploy" karein).

---

## Step 2 — Render par env vars

### Option A (easiest): Blueprint se auto-generate

`render.yaml` mein `generateValue: true` hai — jab aap blueprint apply
karein Render khud strong random values bana dega:
- `SESSION_SECRET`, `ADMIN_PASSWORD`, `ADMIN_TOKEN`

Phir **Render Dashboard → your service → Environment** mein jaake
`ADMIN_PASSWORD` aur `ADMIN_TOKEN` ki values copy karein.
**Admin URL** banega: `https://<aapki-site>/<ADMIN_TOKEN>/login`

### Option B (manual): Neeche ki values use karo

Agar aap khud set karna chahte hain (Dashboard → Environment → add var):

| Variable | Value |
|---|---|
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `aHDmKXtk8te6ioZIangHyGUV` |
| `ADMIN_TOKEN` | `5-gi5tTkl4b3G2p5p-keWw` |
| `SESSION_SECRET` | `kXAJVkS5IbL9UqWwzxuRhO29cuuQt5FceExBCQlhK8xhZ7DwwumzS82Lw6xuzkF2` |
| `UPI_ID` | apna UPI ID |
| `SELLER_PHONE` | apna phone |
| `SELLER_WHATSAPP` | apna WhatsApp |
| `SELLER_EMAIL` | apna email (⚠️ verify karein — README aur render.yaml mein 2 alag emails the; sahi wali set karein) |
| `RAZORPAY_KEY_ID` | Razorpay se (dekhne ke liye niche) |
| `RAZORPAY_KEY_SECRET` | Razorpay se (dekhne ke liye niche) |

---

## Step 3 — Razorpay keys rotate karo

Purane test keys public the. Razorpay Dashboard (dashboard.razorpay.com)
→ **Settings → API Keys** → "Regenerate Key" karein, naye keys upar
Step 2 mein set karein.

- **Abhi testing chahiye:** naye `rzp_test_...` keys use karo
- **Real payment shuru karne par:** `rzp_live_...` keys + Razorpay account
  verification live mode ke liye

> Razorpay keys set NAHI kiye toh koi problem nahi — site sirf manual UPI
> QR payment mode mein chalega (Buy page par QR + contact details dikhengi).

---

## Step 4 — Verify

1. Site kholo → storefront sahi dikhe
2. `https://<site>/<ADMIN_TOKEN>/login` par naye password se login
3. `https://<site>/manifest.json` → ab **404** aana chahiye (pehle token deta tha)
4. Kisi bhi page ke headers mein `Content-Security-Policy`,
   `X-Content-Type-Options: nosniff` hona chahiye (DevTools → Network)
5. Admin panel se test note upload/delete karo — form sahi chal raha hai?
6. **Razorpay test payment** end-to-end: kisi note par Pay → test card se
   payment → success page → Library mein bundle unlocked

---

## ⚠️ Yaad rakhein

- **Data backup:** Render free tier har deploy par naye purchases/users
  reset kar deta hai (README → Data Persistence). Rozana Google Sheet/
  drive mein purchases ka manual record rakhein (admin Purchase page +
  DB se), ya paid persistent disk/S3 par jaayein.
- **Admin URL sirf aapko pata hona chahiye** — naya token ab sirf Render
  Dashboard + aapke notes mein hai, kisi public file mein nahi.
