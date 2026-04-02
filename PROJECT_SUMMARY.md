# GentleEase Project Summary

**GentleEase** is a comprehensive, compassionate mobile health companion application designed to assist users (particularly the elderly or those needing consistent medical tracking) in managing their daily health routines securely and conveniently. 

## 📂 File Structure Overview

The project is split cleanly into three main directory pillars:

### 1. `frontend/` (Mobile Application)
Built using **React Native** and the **Expo** framework (using Expo Router).
- **`app/(tabs)/index.tsx`**: The core component acting as a Single Page App. It handles screen state routing locally (Dashboard, Medication Page, Vault Page, Chatbot Page) to prevent slow loading times.
- **`package.json`**: Holds dependencies like `@expo/vector-icons` for UI resources, `react-native-webview` for STT processing, and `expo-speech` for TTS output.

### 2. `backend/` (Data API Server)
Built using Python and **FastAPI**.
- **`api.py`**: The main server entry point routing all network traffic. It handles GET/POST/DELETE sequences for the database and receives payload data from the Chatbot.
- **`models.py`**: Pydantic data schemas defining exactly how data (Medications, Health Records, Chat Messages) must be sent across the network.
- **`database.py` & `gentleease.db`**: Connectors and persistent memory using a lightweight disk-based SQLite relational database.

### 3. `gentleease-chatbot/` (AI Inference Engine)
A dedicated module directly imported into the backend representing the AI's "brain."
- **`model_loader.py`**: Responsible for spinning up the local generative AI model and managing text completions.
- **`voice_chat.py`**: Local backend fallback methods for audio processing.

---

## 🤖 AI Technologies & Integration map

The AI integration doesn't rely strictly on a single cloud provider. Instead, it pieces together multiple independent functional "senses".

### 1. The Brain (Generative Text)
- **Where it is:** Server-side (`backend/api.py` hooking into `gentleease-chatbot`).
- **How it works:** When a user sends a message from the frontend, it posts to the backend's `/chat` endpoint. The backend invokes the generative model (loaded dynamically by `model_loader.py`). The model parses the context array and spits out a compassionate health-focused text response.
- **Fallback:** If the heavy AI model fails to start or network stalls, `api.py` possesses hardcoded Regex fallback paths (detecting words like "pain" or "medicine") to ensure the user always receives a comforting response.

### 2. The Ears (Speech-to-Text / STT)
- **Where it is:** Client-side (`frontend/app/(tabs)/index.tsx`).
- **How it works:** Real-time speech transcription avoids audio upload latency entirely. The frontend utilizes a hidden `<WebView>` container executing raw HTML/JS that accesses the browser-native **Web Speech API** (`webkitSpeechRecognition`). As the user speaks, intermediate words are asynchronously zipped directly into the frontend `TextInput` state exactly like a native Google voice keyboard.

### 3. The Voice (Text-to-Speech / TTS)
- **Where it is:** Client-side (`frontend/app/(tabs)/index.tsx`).
- **How it works:** The AI model returns an intelligent text response. Upon receiving the string payload, the frontend uses the `expo-speech` library (`Speech.speak()`) to interface with the native iOS/Android system accessibility voices to recite the message aloud at a slightly lowered speech-rate (`rate: 0.85`) optimized for elderly listening comprehension.
