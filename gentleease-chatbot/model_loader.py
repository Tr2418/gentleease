from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time


class ModelWrapper:
    """
    Wraps the tokenizer + model so api.py can call AI_MODEL.generate(text).
    """
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def generate(self, text: str) -> str:
        """Generate a reply for the given user text."""
        # Build a simple prompt
        prompt = (
            "You are GentleEase, a warm and patient AI health companion for elderly users. "
            "Always reply briefly, clearly, and kindly.\n"
            f"User: {text}\nAssistant:"
        )
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=120,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        try:
            from guardrails import apply_elder_care_guardrails, get_special_response
        except ImportError:
            def apply_elder_care_guardrails(r): return r
            def get_special_response(t): return None

        special = get_special_response(text)
        if special:
            return apply_elder_care_guardrails(special)

        # Decode only the newly generated tokens (skip the prompt)
        generated_ids = outputs[0][inputs.shape[-1]:]
        reply = self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        
        # Stop hallucinating extra dialogue lines
        for stop_word in ["\nUser:", "User:", "\nAssistant:", "Assistant:"]:
            if stop_word in reply:
                reply = reply.split(stop_word)[0].strip()

        reply = apply_elder_care_guardrails(reply)
        return reply or "I'm here to help! Could you tell me more?"


def load_model() -> ModelWrapper:
    """Download (or load from cache) TinyLlama and return a ModelWrapper."""
    print("📥 Loading TinyLlama model (may take a moment on first run)...")
    start = time.time()

    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    model.eval()

    print(f"✅ Model loaded in {time.time() - start:.1f}s")
    return ModelWrapper(tokenizer, model)


if __name__ == "__main__":
    m = load_model()
    print(m.generate("How are you?"))
