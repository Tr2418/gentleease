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

from guardrails import apply_elder_care_guardrails, get_special_response

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
