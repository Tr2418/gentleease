import sys
import os

# Dynamically add user site-packages (works on any Windows machine, not hardcoded)
import site
for sp in site.getsitepackages():
    if sp not in sys.path:
        sys.path.append(sp)

import pyttsx3
import speech_recognition as sr
import requests
import json
import time

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Slower speech for clarity
tts_engine.setProperty('volume', 1.0)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# ── Backend URL ───────────────────────────────────────────────────────────────
# Change this to your backend's IP if running on a different machine
API_BASE = os.environ.get("GENTLEEASE_API", "http://127.0.0.1:8000")

def speak(text):
    """Convert text to speech."""
    print(f"🤖 Speaking: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen for voice input and convert to text."""
    try:
        with sr.Microphone() as source:
            print("👂 Listening... (Speak now)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)

        print("🔄 Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        error_msg = "Sorry, I didn't understand that. Could you repeat?"
        print(f"❌ {error_msg}")
        speak(error_msg)
        return None
    except sr.RequestError:
        error_msg = "Sorry, speech service is unavailable."
        print(f"❌ {error_msg}")
        speak(error_msg)
        return None
    except Exception as e:
        error_msg = f"Error with microphone: {str(e)}"
        print(f"❌ {error_msg}")
        speak(error_msg)
        return None

def chat_with_bot(message):
    """Send message to the GentleEase backend API and return reply."""
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={"message": message},
            timeout=10
        )
        if response.status_code == 200:
            # Fixed Bug #2: key is "reply" (not "response") — matches api.py
            bot_response = response.json()["reply"]
            return bot_response
        else:
            return "Sorry, I couldn't connect to my brain right now."
    except Exception as e:
        print(f"❌ API Error: {e}")
        return "Sorry, I'm having trouble thinking right now."

def voice_assistant():
    """Main voice assistant loop."""
    speak("Hello! I'm your GentleEase assistant. How can I help you today?")

    while True:
        print("\n--- Voice Assistant Active ---")
        print("🎤 Say something (or say 'exit' to quit)")

        user_input = listen()

        if user_input is None:
            continue

        if 'exit' in user_input.lower() or 'quit' in user_input.lower():
            speak("Goodbye! Take care!")
            break

        print("💭 Thinking...")
        bot_response = chat_with_bot(user_input)

        speak(bot_response)
        print(f"🤖 Bot: {bot_response}")

if __name__ == "__main__":
    print("🚀 Starting Voice Assistant...")
    print(f"💡 Make sure your chatbot server is running at {API_BASE}")
    try:
        voice_assistant()
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
