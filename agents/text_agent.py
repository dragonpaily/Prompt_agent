import google.generativeai as genai

# Initialize the model for this agent
try:
    text_worker_model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    print(f"Error initializing text worker model: {e}")
    text_worker_model = None

def generate_text(refined_prompt):
    """
    Calls the Gemini API to generate text.
    """
    if not text_worker_model:
        print("Text worker model is not initialized.")
        return

    print(f"\n🚀 Sending to text worker...")
    print(f"   Final Prompt: \"{refined_prompt}\"")
    print("-" * 20)
    
    try:
        response = text_worker_model.generate_content(refined_prompt)
        print("✅ Generation Complete:\n")
        print(response.text)
    except Exception as e:
        print(f"Error during text generation: {e}")
        
    print("-" * 20)