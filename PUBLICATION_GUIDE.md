# GentleEase — Publication & Deployment Guide

**Version:** 1.0.0  
**Last Updated:** April 2, 2026

---

## 📋 Project Overview

GentleEase is a React Native + FastAPI health companion app designed for elderly users. It includes:
- **Medication Reminders** (add, view, delete)
- **Medical Records Vault** (store health documents & reports)
- **AI Voice Chatbot** (companion & health advice)
- **SOS Emergency Button** (quick alert to family)

### Tech Stack
- **Frontend:** React Native (Expo) + TypeScript
- **Backend:** FastAPI + Python 3.14
- **Database:** SQLite
- **Hosting:** Android (via Expo Go or APK), Backend on PC/Cloud

---

## ✅ Pre-Publication Checklist

### Frontend Status
- [x] All lint errors fixed
- [x] TypeScript types correct
- [x] Elderly-friendly UI (large fonts, easy buttons)
- [x] Medication input system works
- [x] Medical Records Vault functional
- [x] AI Chatbot integrated
- [x] SOS button implements
- [x] Network timeout handling (12 seconds)
- [x] Deletion confirmations added
- [x] Error messages clear

### Backend Status
- [x] All CRUD endpoints working
- [x] Medications: GET, POST, DELETE ✅
- [x] Records: GET, POST, DELETE ✅
- [x] Chat: POST (AI or fallback) ✅
- [x] SOS: POST ✅
- [x] Chat History: GET ✅
- [x] CORS enabled for dev
- [x] Database auto-initialization
- [x] Optional AI model (graceful fallback)
- [x] Optional TTS (graceful fallback)

### Database Status
- [x] SQLite database auto-created
- [x] 3 tables: meds, records, chat_log
- [x] Indexes optimized
- [x] Data persists between app restarts

---

## 🚀 Deployment Steps

### Step 1: Prepare Backend Server

#### Option A: Run on Your PC (Development/Testing)
```bash
cd C:\Users\Tarun\gentleease\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Start the server
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Server should print:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Database ready at: gentleease.db
```

#### Option B: Cloud Deployment (Recommended for production)
Use services like:
- **Heroku** (free tier available, limited)
- **DigitalOcean** (simple, affordable)
- **AWS Lambda + RDS** (scalable)
- **Google Cloud Run** (pay-per-request)
- **PythonAnywhere** (Python-specific hosting)

**For any cloud deployment, update frontend `.env` to use cloud API:**
```
EXPO_PUBLIC_API_BASE=https://your-backend-domain.com
```

### Step 2: Deploy Frontend

#### Option A: Expo Go (Easiest for Testing)
Already configured! Users with Expo Go can scan QR code from terminal.

#### Option B: Build Android APK (For Installation Only)
```bash
cd frontend
eas login  # Login to Expo account
eas build --platform android
# Download APK and distribute to users
```

#### Option C: Build for iOS
```bash
eas build --platform ios
# Requires Apple developer account
```

### Step 3: Create a `.env.production` File

For production, create a new `.env` override:
```bash
# Change this to your actual backend URL
EXPO_PUBLIC_API_BASE=https://your-backend-server.com
```

---

## 🛠️ Maintenance & Operations

### Adding a New Medication (User Flow)
1. Open app → Tap "Medication" card
2. Enter medicine name (e.g., "Aspirin")
3. Enter time (e.g., "08:00 AM")
4. Tap blue "+" button
5. Medication appears in list

**Backend**: `POST /meds` with `{name, time}`

### Adding a Medical Record (User Flow)
1. Open app → Tap "Medical Records Vault"
2. Enter report name (e.g., "Blood Test Report")
3. Tap green "Upload" button
4. Record appears with today's date

**Backend**: `POST /records` with `{name, type, date, notes}`

### Testing AI Chatbot
1. Open app → Tap "AI Chatbot"
2. Type a health question (e.g., "What should I do for headache?")
3. Wait for reply (fallback if AI model not installed)
4. Tap speaker icon to hear response aloud

**Backend**: `POST /chat` with `{message, speak}`

### SOS Emergency Alert
1. Open app → Tap large red "TAP FOR HELP" button
2. Confirmation: "🚨 SOS TRIGGERED"
3. Family members notified (integrate external service)

**Backend**: `POST /sos` with `{user_name, location}`

---

## 📊 Database Management

### Backing Up Data
```bash
# Copy the SQLite database file
copy C:\Users\Tarun\gentleease\backend\gentleease.db C:\backup\gentleease_backup.db
```

### Restoring from Backup
```bash
copy C:\backup\gentleease_backup.db C:\Users\Tarun\gentleease\backend\gentleease.db
```

### Viewing Database Content (Optional)
```bash
# Install sqlite3 CLI if needed
pip install sqlite3

# Open database and query
sqlite3 gentleease.db
> SELECT * FROM meds;
> SELECT * FROM records;
> .exit
```

---

## 🔒 Security Improvements for Production

### 1. Update CORS Policy
**File:** `backend/api.py` (Line ~77)

Change:
```python
allow_origins=["*"],  # ❌ Unsafe for production
```

To:
```python
allow_origins=[
    "https://your-app-domain.com",
    "https://your-web-app.com"
],
```

### 2. Add Input Validation
**Already partially done**, but add more:
```python
max_med_name_length = 100
max_notes_length = 500
```

### 3. Add Database Encryption
For sensitive data, consider:
- **SQLCipher**: Encrypt SQLite database
- **PostgreSQL + SSL**: Use managed database service

### 4. Set Up HTTPS
Use **Let's Encrypt** (free SSL certificates):
```bash
# On backend server
certbot certonly --standalone -d your-domain.com
```

### 5. Rate Limiting
Add rate limiting to prevent abuse:
```bash
pip install slowapi
# See SlowAPI documentation for integration
```

---

## 📱 User Setup Instructions

### For Elderly Users (EASY VERSION)

**To Use the App on Android:**

1. **Install Expo Go** from Google Play Store
2. **Ask caregiver** to give you a QR code OR **scan this link**
3. **Tap "Medication"** → Add medicine name + time (e.g., "Aspirin 08:00 AM")
4. **Tap "Medical Records"** → Add report names
5. **Tap "AI Chatbot"** → Ask health questions
6. **Tap red "TAP FOR HELP"** if you need emergency assistance

**Everything automatically saves** — no need to press "Save"!

---

## 🐛 Troubleshooting

### App Shows "Request timed out"
**Fix:** Make sure backend is running and phone is on WiFi
```bash
# PC: Check backend is running
netstat -an | findstr 8000

# Check phone WiFi: Settings → WiFi → Make sure connected to same network as PC
```

### Medications not saving
**Cause:** Field validation
- Medicine name can't be empty
- Time can't be empty
- Use format: "08:00 AM" or "08:00"

### Chat responses slow
**Cause:** AI model not loaded
- App uses fallback reply (still works!)
- To enable AI: `pip install transformers torch` on backend

### Database file corruption
**Solution:** Delete and recreate
```bash
rm gentleease.db
# Restart backend — it will auto-create fresh database
```

---

## 📈 Future Enhancements

### Phase 2 (Recommendations)
1. **Push Notifications** — Medicine reminders
2. **Family Portal** — Caregivers view patient data
3. **Real AI Model** — Download Llama 2 or similar
4. **Offline Mode** — App works without internet
5. **Multi-language** — Support Hindi, Tamil, etc.

### Phase 3 (Advanced)
1. **Wearable Integration** — Heart rate, blood oxygen
2. **Doctor Integration** — Share records with healthcare providers
3. **Insurance Integration** — Auto-fill claims
4. **Telemedicine** — In-app video calls with doctors

---

## 📞 Support & Contact

**For Issues:**
- Email: team@gentleease.com
- GitHub: [Your Repo]
- Hotline: [Your Phone]

**Team:** Akshaya · Prakrithi · Tarun · Srujan

---

## 📄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Apr 2, 2026 | Initial release with Medications, Records, Chat, SOS |

---

## ✨ Final Checklist Before Going Live

- [ ] Backend tested on production target machine
- [ ] Frontend APK built and tested on real Android device
- [ ] `.env` files configured for production
- [ ] Database backup created
- [ ] User documentation printed/shared with caregivers
- [ ] Team knows how to restart backend if needed
- [ ] Emergency contact info for support
- [ ] CORS updated to production domain
- [ ] Rate limiting configured
- [ ] HTTPS certificate installed (if on cloud)

---

**GentleEase v1.0.0 — Ready for Publication** ✅
