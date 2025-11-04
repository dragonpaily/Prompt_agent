import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file to get the API key
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key or api_key == "YOUR_API_KEY_GOES_HERE":
    print("ERROR: GOOGLE_API_KEY not found or not set in .env file.")
else:
    try:
        genai.configure(api_key=api_key)
        
        print("Fetching available models for your API key...\n")
        
        found_models = False
        # List all models
        for m in genai.list_models():
            # We only care about models that can 'generateContent'
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Found usable model:")
                print(f"   Model Name: {m.name}\n")
                found_models = True

        if not found_models:
            print("❌ No models are available for 'generateContent' with your API key.")
        
        print("\n--- End of List ---")

    except Exception as e:
        print(f"An error occurred while trying to list models: {e}")