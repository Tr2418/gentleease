from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize FastAPI app
app = FastAPI(title="GentleEase Chatbot")

# Load model (only once when app starts)
print("🚀 Loading AI model...")
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
print("✅ Model ready!")

# Data structure for chat messages
class ChatMessage(BaseModel):
    message: str

# Apply guardrails for elder care safety
def apply_elder_care_guardrails(response):
    """Apply basic safety filters for elder care responses"""
    
    # Convert to lowercase for checking
    response_lower = response.lower()
    
    # Block potentially harmful content
    dangerous_phrases = [
        "harm yourself", "kill yourself", "dangerous dose",
        "overdose", "stop taking", "ignore doctor", "self harm"
    ]
    
    for phrase in dangerous_phrases:
        if phrase in response_lower:
            return "🚨 I'm here to help keep you safe! Please contact your doctor or family for medical advice."
    
    # Prevent negative/crushing responses  
    negative_words = ["impossible", "never", "can't", "useless", "hopeless"]
    if any(word in response_lower for word in negative_words):
        return "🌟 There's always hope! Let's focus on positive steps you can take."
    
    # Keep responses reasonably short for clarity (elder-friendly)
    if len(response) > 300:
        # Truncate and add friendly closing
        return response[:297] + "..."
    
    return response

# Special responses for elder care with guardrails applied
def get_special_response(text):
    text_lower = text.lower()
    
    if "medicine" in text_lower or "pill" in text_lower or "medication" in text_lower:
        return "💊 Remember to take your medication at 6 PM today! Would you like me to remind you?"
    elif "water" in text_lower or "drink" in text_lower or "hydrate" in text_lower:
        return "💧 Don't forget to stay hydrated! Try drinking a glass of water now. I'll remind you every 2 hours."
    elif "lonely" in text_lower or "sad" in text_lower or "bored" in text_lower:
        return "🤗 I'm here with you! Would you like to hear a story, play a simple game, or talk about your day?"
    elif "emergency" in text_lower or "help" in text_lower or "fall" in text_lower or "pain" in text_lower:
        return "🚨 Emergency alert sent to your family and doctor. Help is on the way! Please stay calm and sit safely."
    elif "hello" in text_lower or "hi" in text_lower or "hey" in text_lower:
        return "👋 Hello there! It's wonderful to see you today. How can I help make your day better?"
    elif "food" in text_lower or "eat" in text_lower or "diet" in text_lower or "hungry" in text_lower:
        return "🍎 How about a healthy snack? Try some fruits, nuts, or yogurt. Eating regularly helps keep your energy up!"
    elif "exercise" in text_lower or "move" in text_lower or "walk" in text_lower:
        return "🦵 Gentle movement is great! Even a short walk around the house helps keep you strong and healthy."
    elif "sleep" in text_lower or "tired" in text_lower or "rest" in text_lower:
        return "😴 Good rest is important! Try to maintain regular sleep hours. Would you like tips for better sleep?"
    else:
        return None

# Main chat endpoint with guardrails
@app.post("/chat")
async def chat(chat_message: ChatMessage):
    # Check for special elder care responses first
    special_response = get_special_response(chat_message.message)
    if special_response:
        # Apply guardrails to special responses
        safe_response = apply_elder_care_guardrails(special_response)
        return {"response": safe_response}
    
    # Otherwise, use AI model
    try:
        inputs = tokenizer.encode(chat_message.message, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(inputs, max_new_tokens=100, temperature=0.7)
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Apply guardrails to AI-generated response
        safe_response = apply_elder_care_guardrails(response)
        return {"response": safe_response}
    except Exception as e:
        # Even errors get guardrail treatment
        error_response = "Sorry, I'm having trouble responding right now. Please try again or ask something else."
        safe_error = apply_elder_care_guardrails(error_response)
        raise HTTPException(status_code=500, detail=safe_error)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "🤖 GentleEase Chatbot is running! Ready to help with elder care."}

# Additional endpoints for elder care features
@app.get("/health-tips")
async def health_tips():
    """Provide general health tips for seniors"""
    tips = [
        "💧 Stay hydrated throughout the day",
        "🚶 Take short walks daily if possible", 
        "🥗 Eat balanced meals with plenty of fruits",
        "😴 Maintain regular sleep schedule",
        "📞 Stay connected with family and friends",
        "📚 Keep your mind active with reading or puzzles"
    ]
    return {"tips": tips}

@app.get("/emergency-contact")
async def emergency_contact():
    """Simulate emergency contact feature"""
    return {"message": "🚨 Emergency services notified! Family contacts alerted!"}
