import os
import google.generativeai as genai
from dotenv import load_dotenv

def load_api_key():
    """
    Loads the Google API key from the .env file and configures the genai library.
    Returns True on success, False on failure.
    """
    # Load environment variables from .env file
    load_dotenv() 
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key or api_key == "YOUR_API_KEY_GOES_HERE":
        print("="*50)
        print("ERROR: 'GOOGLE_API_KEY' not found in .env file.")
        print("Please create a .env file and add your API key.")
        print("="*50)
        return False
        
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Google API: {e}")
        return False
    