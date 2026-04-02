# GentleEase Run Instructions

Follow these step-by-step instructions to get both the Backend server and Frontend Expo application running concurrently on your local machine.

## Prerequisites
- Node.js and npm installed.
- Python 3.9+ installed.
- Expo Go installed on your mobile device (if testing physically), or Android Studio / Xcode for emulation.

---

## 1. Start the Backend API (Terminal 1)

The backend handles the database, AI chat interactions, and data storage. It runs on FastAPI.

1. Open a new terminal.
2. Navigate to the backend directory:
   ```bash
   cd c:\Users\tarun\gentleease\backend
   ```
3. *(Optional but recommended)* Activate your Python virtual environment if you are using one.
4. Install the required Python dependencies (if you haven't already):
   ```bash
   pip install -r requirements.txt
   ```
5. Start the Uvicorn server:
   ```bash
   python -m uvicorn api:app --reload --port 8000
   ```
   > **Note on Mobile Devices:** If you are testing on a physical mobile device, your phone must be on the same WiFi network as your computer, and you must bind the host to `0.0.0.0` so the phone can reach it:  
   > `python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000`

---

## 2. Start the Frontend App (Terminal 2)

The frontend is an Expo-managed React Native application.

1. Open a second, separate terminal.
2. Navigate to the frontend directory:
   ```bash
   cd c:\Users\tarun\gentleease\frontend
   ```
3. Install Node dependencies (if you haven't already):
   ```bash
   npm install
   ```
4. Start the Expo development server (clearing the cache prevents stale configuration issues):
   ```bash
   npx expo start --clear
   ```
5. A QR code will generate in your terminal.
   - **Android:** Scan the QR code using the Expo Go app.
   - **iOS:** Scan the QR code using your default Camera app and open it in Expo Go.
   - **Emulator:** Press `a` for Android Emulator or `i` for iOS Simulator directly in the terminal.

---

## 🛑 Troubleshooting 

- **"Port 8081 already in use" (Frontend):** 
  If you attempt to start Expo and receive a port conflict, an old process is hanging. Kill the existing node process. On Windows PowerShell, you can run:
  ```powershell
  Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*expo*" } | Stop-Process -Force
  ```
- **"Network request failed" (Frontend to Backend):** 
  Double-check that the Python backend is running, and if utilizing a physical device, ensure you started the backend server with `--host 0.0.0.0` and that your mobile device is on the exact same Wi-Fi network.
