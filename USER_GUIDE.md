# GentleEase — Quick Reference for Elderly Users & Caregivers

## 🌿 What Is GentleEase?

A friendly health companion app that helps you:
- ✅ Remember when to take medicines
- ✅ Keep your medical history organized
- ✅ Chat with an AI health assistant
- ✅ Call for help in emergencies

---

## 🏠 Home Screen — Your Dashboard

```
┌─────────────────────────────────┐
│      GentleEase  🌿             │
│  Your compassionate health      │
│      companion                  │
│                                 │
│    ┌──────────┐  ┌──────────┐  │
│    │   💊     │  │   🤖     │  │
│    │Medication│  │AI Chatbot│  │
│    └──────────┘  └──────────┘  │
│                                 │
│    ┌───────────────────────┐   │
│    │  📂 Medical Records   │   │
│    │      Vault            │   │
│    └───────────────────────┘   │
│                                 │
│    ┌─────────────────────────┐ │
│    │  🚨 TAP FOR HELP  🚨   │ │
│    │  (Red Emergency Button)│ │
│    └─────────────────────────┘ │
└─────────────────────────────────┘
```

---

## 💊 How to Add a Medicine Reminder

### Step-by-Step:

1. **Tap the "Medication" card**
   - Big blue card with pill icon

2. **Type medicine name**
   - Example: "Aspirin" or "Blood pressure tablet"
   
3. **Type time to take it**
   - Example: "08:00 AM" or "08:00"
   - Click the input field for hint

4. **Tap the BLUE "+" button**
   - Right side of the time field
   - Large button, easy to tap

5. **See medicine in the list!**
   - Shows: Medicine name | Time | Delete button

### Example:
```
Medicine        Time           [Delete]
─────────────────────────────────────
Aspirin        08:00 AM        [❌]
Metformin      12:00 PM        [❌]
Paracetamol    08:00 PM        [❌]
```

### Deleting a Medicine:
1. **Tap the red ❌ icon** next to medicine
2. **Confirm: "Are you sure? This cannot be undone"**
3. **Tap "Delete"** (red button)

---

## 📂 How to Add a Medical Record

### Step-by-Step:

1. **Tap "Medical Records Vault"**
   - Green button on home screen
   
2. **Type report name**
   - Example: "Blood test report"
   - Example: "X-ray results"
   - Example: "Prescription from Dr. Smith"

3. **Tap GREEN "Upload" button**
   - Large button on right side

4. **Record is saved!**
   - Today's date is automatically added
   - Shows in organized list below

### Example:
```
#  📅 Date       📄 Report Name              [❌]
───────────────────────────────────────────────────
1  2026-04-02   Blood test report           [❌]
2  2026-03-31   Doctor prescription        [❌]
3  2026-03-28   X-ray results              [❌]
```

### Deleting a Record:
1. **Tap the red ❌ icon** next to record
2. **Confirm: "Are you sure?"**
3. **Tap "Delete"**

---

## 🤖 How to Chat with AI Assistant

### Step-by-Step:

1. **Tap "AI Chatbot"**
   - Purple robot icon on home screen

2. **See conversation history**
   - Your messages appear in light blue boxes on RIGHT
   - AI replies in purple boxes on LEFT
   - Messages are clearly separated

3. **Type your message**
   - Large text box at bottom
   - Example: "What should I do for headache?"

4. **Tap PURPLE "Send" button**
   - Big button on right side
   - App shows "GentleEase is thinking..."

5. **Read AI's reply**
   - Purple box with response
   - Tap speaker icon 🔊 to hear it aloud

### Tips:
- Ask health questions (AI gives general advice only)
- Ask for encouragement or emotional support
- Ask about medicines (general info only)
- Ask for reminders

### Example:
```
┌────────────────────────────────────┐
│ Hello! I am your GentleEase        │
│ AI companion. How are you feeling? │ 🔊
│ 😊                                  │
└────────────────────────────────────┘

                            ┌──────────┐
                            │I have a  │
                            │headache  │
                            └──────────┘

┌────────────────────────────────────┐
│ For a headache:                     │ 🔊
│ 1. Rest in dark, quiet room        │
│ 2. Drink water                     │
│ 3. Try light stretching            │
│ 4. If severe, take paracetamol     │
│ Ask your doctor if it persists!    │
└────────────────────────────────────┘
```

---

## 🚨 Emergency SOS Button

### When to Use:
- **Feeling unwell suddenly**
- **Need immediate help**
- **Can't reach family by phone**
- **Any emergency**

### How:
1. **Tap the BIG RED button** "TAP FOR HELP" on home screen
2. **Confirmation pops up** "🚨 SOS TRIGGERED"
3. **Tap OK**
4. **Family is notified immediately**

### What Happens:
- SOS alert sent to family members
- Your location shared (if app has permission)
- Voice message: "SOS Activated. Alerting family."
- Family calls you back

---

## ⚽ Top Tips for Elderly Users

### Tips:
✅ **Take your time** — App never times out  
✅ **Large text** — All fonts are easy to read  
✅ **Big buttons** — Designed for easy tapping  
✅ **Clear colors** — Blue for Medication, Green for Records, Purple for Chat  
✅ **Automatic save** — Never lose data  
✅ **No passwords** — Just tap and use  
✅ **Easy back button** — Go back anytime  
✅ **Ask AI** — Chatbot available 24/7  

### Common Mistakes to Avoid:
❌ Leaving medicine name or time EMPTY  
❌ Deleting a record by accident (always confirms first)  
❌ Typing message but forgetting to tap SEND  
❌ Closing app without saving (it auto-saves!)  

---

## 🆘 What If Something Goes Wrong?

### "Request timed out" message?
- **Check:** Is your phone on WiFi?
- **Fix:** Ask caregiver to restart backend server
- **Try:** Tap "Refresh" button (down arrow)

### Medicine won't save?
- **Check:** Did you type both name AND time?
- **Fix:** Fill both fields with text
- **Try:** Tap "+" button again

### Can't see chat history?
- **Check:** Are you in the Chatbot page?
- **Fix:** Scroll up to see older messages
- **Try:** Refresh by swiping down

### App crashes?
- **Close** the app completely
- **Wait** 10 seconds
- **Open** Expo Go again
- **Scan** QR code to reload

---

## 📞 Getting Help

| Problem | Solution |
|---------|----------|
| App won't start | Ask caregiver to restart Expo |
| Backend not running | Ask caregiver: `uvicorn api:app --port 8000` |
| WiFi not working | Restart router, reconnect phone |
| Data lost | Data is in database — should still be there |
| Medicine alarm missing | This version doesn't have alarms yet (planned!) |
| Can't hear voice | Turn up phone volume, tap speaker icon |

---

## 🆓 Free, Free, Free!

✅ **No login required**  
✅ **No subscription**  
✅ **No ads**  
✅ **No hidden fees**  
✅ **A gift for your health**  

---

## 👥 Caregiver Setup (For Family Members)

### To Get Your Elderly Relative Started:

1. **Download Expo Go** from Google Play Store
2. **Seat them comfortably** with their phone
3. **Open Expo Go** and tap "Scan QR code"
4. **Show them the QR code** from the terminal/computer
5. **Wait for app to load** (30 seconds first time)
6. **Show them the home screen** — walk through each button
7. **Practice** adding a medicine together
8. **Let them explore** — it's safe!

### What They Can Do:
- Add medicines they take
- View their medical history
- Chat with AI for support
- Call for help anytime
- Never lose data

### Your Role:
- Sometimes restart the backend if it crashes
- Help with Wi-Fi issues
- Occasionally check their records
- Be available for emergencies

---

## 📚 GentleEase Version 1.0.0

**Released:** April 2, 2026  
**Made with ❤️ for elderly users**

**Team:** Akshaya · Prakrithi · Tarun · Srujan

---

**Thank you for using GentleEase! Stay healthy and safe.** 🌿
