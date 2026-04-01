"""
GentleEase Backend — FastAPI + SQLite
Run with:  uvicorn api:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
import sys, os

# ── Import our own files ───────────────────────────────────────────────────────
from database import init_db, get_connection
from models import (
    Med, MedCreate,
    Record, RecordCreate,
    ChatMessage, ChatResponse,
    SOSAlert,
)

# ── Optional chatbot integration (lazy-loaded) ───────────────────────────────
CHATBOT_PATH = os.path.join(os.path.dirname(__file__), "..", "gentleease-chatbot")
sys.path.insert(0, os.path.abspath(CHATBOT_PATH))

AI_MODEL = None


def get_ai_model():
    global AI_MODEL
    if AI_MODEL is not None:
        return AI_MODEL
    try:
        from model_loader import load_model

        AI_MODEL = load_model()  # returns ModelWrapper with .generate()
        print("✅ AI model loaded")
        return AI_MODEL
    except Exception as e:
        # Keep quiet-ish; app still works with fallback.
        print(f"⚠️  AI model unavailable: {e}")
        AI_MODEL = None
        return None


def try_speak(text: str) -> bool:
    """Attempt TTS using gentleease-chatbot/voice_chat.py. Returns True if spoken."""
    try:
        from voice_chat import speak

        speak(text)
        return True
    except Exception as e:
        print(f"⚠️  TTS unavailable: {e}")
        return False

# ── App setup ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Replaces the deprecated @app.on_event('startup')."""
    init_db()
    yield

app = FastAPI(
    title="GentleEase API",
    description="Backend for the GentleEase health companion app",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow requests from your Expo app (any origin during dev is fine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # In production, replace "*" with your app's URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Root / Health check ───────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "GentleEase backend is running ✅"}


# ══════════════════════════════════════════════════════════════════════════════
# MEDICATIONS  (/meds)
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/meds", response_model=List[Med])
def get_all_meds():
    """Return all saved medications."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM meds ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/meds", response_model=Med)
def add_med(med: MedCreate):
    """Add a new medication reminder."""
    if not med.name.strip():
        raise HTTPException(status_code=400, detail="Medicine name cannot be empty.")
    if not med.time.strip():
        raise HTTPException(status_code=400, detail="Time cannot be empty.")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO meds (name, time) VALUES (?, ?)",
        (med.name.strip(), med.time.strip()),
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM meds WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)


@app.delete("/meds/{med_id}")
def delete_med(med_id: int):
    """Delete a medication by its ID."""
    conn = get_connection()
    result = conn.execute("DELETE FROM meds WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Med not found.")
    return {"message": f"Med {med_id} deleted ✅"}


# ══════════════════════════════════════════════════════════════════════════════
# HEALTH RECORDS  (/records)
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/records", response_model=List[Record])
def get_all_records():
    """Return all health records."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM records ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/records", response_model=Record)
def add_record(record: RecordCreate):
    """Add a new health record entry."""
    if not record.name.strip():
        raise HTTPException(status_code=400, detail="Record name cannot be empty.")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO records (name, type, date, notes) VALUES (?, ?, ?, ?)",
        (record.name.strip(), record.type, record.date, record.notes),
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM records WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return dict(row)


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    """Delete a health record by its ID."""
    conn = get_connection()
    result = conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Record not found.")
    return {"message": f"Record {record_id} deleted ✅"}


# ══════════════════════════════════════════════════════════════════════════════
# AI CHAT  (/chat)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/chat", response_model=ChatResponse)
def chat(msg: ChatMessage):
    """
    Send a message to the AI companion and get a reply.
    Optionally speaks the reply aloud if speak=true.
    """
    user_text = msg.message.strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # ── Generate reply ─────────────────────────────────────────────────────
    model = get_ai_model()
    if model is not None:
        try:
            reply = model.generate(user_text)
        except Exception as e:
            reply = f"Sorry, I had trouble thinking. Error: {str(e)}"
    else:
        # Friendly fallback when the AI model isn't loaded
        # Provide helpful, elderly-friendly responses
        user_lower = user_text.lower()
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'how are you']):
            reply = "Hello! I'm here and happy to chat with you. How can I help you today? 😊"
        elif any(word in user_lower for word in ['headache', 'pain', 'hurt', 'ache', 'sick', 'ill']):
            reply = "I'm sorry you're not feeling well. Please stay hydrated and rest. If the pain is severe or persistent, please contact your doctor. I'm here to listen if you need to talk. 💙"
        elif any(word in user_lower for word in ['medicine', 'medication', 'pill', 'tablet', 'dose']):
            reply = "Questions about your medicines are great! Always follow your doctor's instructions. Check the TIME and DOSAGE on the bottle. If you have doubts, ask your pharmacist. I'm here to help! 💊"
        elif any(word in user_lower for word in ['doctor', 'hospital', 'emergency', 'urgent', 'help']):
            reply = "Your health is important! If this is an emergency, please call your local emergency number or tap the red 🚨 'TAP FOR HELP' button on the home screen. I'm here for support. 🚨"
        elif any(word in user_lower for word in ['thanks', 'thank you', 'help', 'thank']):
            reply = "You're very welcome! I'm always here for you. Remember, taking care of your health is the best thing you can do. Take care! 💚"
        else:
            # Generic warm response
            reply = (
                f"Thank you for sharing: '{user_text}'\n\n"
                "I'm GentleEase, your health companion. "
                "I'm here to listen and support you. "
                "Is there anything specific about your health I can help with?"
            )

    # ── Save to chat log ───────────────────────────────────────────────────
    now = datetime.now().isoformat()
    conn = get_connection()
    conn.execute("INSERT INTO chat_log (role, message, timestamp) VALUES (?, ?, ?)", ("user", user_text, now))
    conn.execute("INSERT INTO chat_log (role, message, timestamp) VALUES (?, ?, ?)", ("assistant", reply, now))
    # Keep only the last 100 messages
    conn.execute("DELETE FROM chat_log WHERE id NOT IN (SELECT id FROM chat_log ORDER BY id DESC LIMIT 100)")
    conn.commit()
    conn.close()

    # ── Optional text-to-speech ────────────────────────────────────────────
    if msg.speak:
        try_speak(reply)

    return {"reply": reply}


@app.get("/chat/history")
def get_chat_history(limit: int = 20):
    """Return recent chat messages."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT role, message, timestamp FROM chat_log ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]


# ══════════════════════════════════════════════════════════════════════════════
# SOS  (/sos)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/sos")
def trigger_sos(alert: SOSAlert):
    """
    SOS button was tapped.
    Logs the event and returns an alert message.
    """
    message = (
        f"🚨 SOS ALERT from {alert.user_name}! "
        f"Location: {alert.location}. "
        "Please check on them immediately."
    )

    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_log (role, message, timestamp) VALUES (?, ?, ?)",
        ("system", f"SOS triggered by {alert.user_name}", datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

    if TTS_AVAILABLE:
        try:
            speak(message)
        except Exception as e:
            print(f"SOS TTS error: {e}")

    print(f"\n{'='*50}\n{message}\n{'='*50}\n")
    return {"status": "SOS sent", "message": message}


# ══════════════════════════════════════════════════════════════════════════════
# VOICE / TTS  (/speak)
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/speak")
def text_to_speech(msg: ChatMessage):
    """Convert any text to speech using voice_chat.py."""
    ok = try_speak(msg.message)
    if not ok:
        raise HTTPException(status_code=503, detail="Voice module not available.")
    return {"status": "spoken ✅"}
