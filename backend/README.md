# GentleEase — Setup Guide (Windows 11 + VS Code)

## Folder structure you should have

```
gentleease/                    ← your mega folder
├── backend/                   ← NEW (this folder)
│   ├── api.py                 ← FastAPI server (all routes)
│   ├── database.py            ← SQLite database setup
│   ├── models.py              ← Data shapes (what is a "med"?)
│   └── requirements.txt       ← Python packages to install
│
├── gentleease-chatbot/        ← your EXISTING chatbot folder
│   ├── main.py
│   ├── model_loader.py
│   └── voice_chat.py
│
└── frontend/                  ← your Expo React Native app (other laptop)
    ├── app/
    ├── components/
    └── ...
```

---

## Step 1 — Create the mega folder

Open VS Code, then open the terminal inside it (Ctrl + ` backtick).

```bash
mkdir C:\Users\Tarun\gentleease
mkdir C:\Users\Tarun\gentleease\backend
```

Copy your `gentleease-chatbot` folder inside `gentleease\` so it looks like the structure above.

---

## Step 2 — Copy the backend files

Copy these 4 files into `gentleease\backend\`:
- api.py
- database.py
- models.py
- requirements.txt

---

## Step 3 — Create a virtual environment for the backend

In the VS Code terminal:

```bash
cd C:\Users\Tarun\gentleease\backend
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the start of the line. That means it worked.

---

## Step 4 — Install packages

```bash
pip install -r requirements.txt
```

Also install whatever your chatbot needs (from its existing venv or requirements):

```bash
pip install pyaudio
```

If pyaudio fails, use the .whl file you already have:

```bash
pip install ..\gentleease-chatbot\pyaudio-0.2.14-cp314-cp314-win_amd64.whl
```

---

## Step 5 — Start the backend server

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Database ready at: gentleease.db
```

---

## Step 6 — Test your API in the browser

Open your browser and go to:

```
http://localhost:8000
```

You should see: `{"status": "GentleEase backend is running ✅"}`

For the full interactive docs (Swagger UI), go to:

```
http://localhost:8000/docs
```

You can test every route there — add a med, delete it, send a chat message, etc.

---

## Step 7 — Connect your Expo frontend

In your React Native app on the other laptop, whenever you call the backend use:

```
http://<YOUR_PC_IP>:8000
```

To find your PC's local IP: open Command Prompt and type `ipconfig`.
Look for `IPv4 Address` — it looks like `192.168.1.X`.

Example API calls from React Native:

```javascript
// Get all meds
const res = await fetch('http://192.168.1.X:8000/meds');
const meds = await res.json();

// Add a med
await fetch('http://192.168.1.X:8000/meds', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Paracetamol', time: '08:00 AM' }),
});

// Delete a med
await fetch(`http://192.168.1.X:8000/meds/${id}`, { method: 'DELETE' });

// Chat
const res = await fetch('http://192.168.1.X:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello!', speak: false }),
});
const data = await res.json();
console.log(data.reply);
```

---

## Quick Reference — All API Endpoints

| Method | URL               | What it does                    |
|--------|-------------------|---------------------------------|
| GET    | /meds             | Get all medications             |
| POST   | /meds             | Add a medication                |
| DELETE | /meds/{id}        | Delete a medication             |
| GET    | /records          | Get all health records          |
| POST   | /records          | Add a health record             |
| DELETE | /records/{id}     | Delete a health record          |
| POST   | /chat             | Send a message to AI            |
| GET    | /chat/history     | Get recent chat history         |
| POST   | /sos              | Trigger SOS alert               |
| POST   | /speak            | Convert text to speech          |

---

## Common Errors and Fixes

**"Module not found: fastapi"**
→ Make sure you activated the venv: `venv\Scripts\activate`

**"Address already in use"**
→ Another process is on port 8000. Stop it or use `--port 8001`

**"Could not load AI model"**
→ The chatbot path needs updating. Open `api.py` and edit `CHATBOT_PATH`.

**Frontend can't reach backend**
→ Make sure both devices are on the same WiFi. Use your PC's IP, not localhost.
