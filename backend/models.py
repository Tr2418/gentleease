from pydantic import BaseModel
from typing import Optional

# ── Medication ─────────────────────────────────────────────────────────────────

class MedCreate(BaseModel):
    """What the frontend sends when adding a new med."""
    name: str
    time: str  # e.g. "08:00 AM"

class Med(BaseModel):
    """What we send back to the frontend."""
    id: int
    name: str
    time: str

# ── Health Record ──────────────────────────────────────────────────────────────

class RecordCreate(BaseModel):
    """What the frontend sends when adding a new health record."""
    name: str
    type: Optional[str] = "General"   # e.g. Blood Test, X-Ray, Prescription
    date: str                          # e.g. "2026-04-02"
    notes: Optional[str] = ""

class Record(BaseModel):
    id: int
    name: str
    type: str
    date: str
    notes: str

# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """A single message sent from the frontend to the AI."""
    message: str
    speak: Optional[bool] = False  # If True, also do text-to-speech

class ChatResponse(BaseModel):
    reply: str

# ── SOS ───────────────────────────────────────────────────────────────────────

class SOSAlert(BaseModel):
    """Payload when SOS button is tapped."""
    user_name: Optional[str] = "User"
    location: Optional[str] = "Unknown"
