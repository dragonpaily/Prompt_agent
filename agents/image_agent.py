import google.generativeai as genai
import pathlib  # For saving the file
import datetime # For unique filenames

# --- THIS IS THE MODEL NAME FROM YOUR LIST ---
MODEL_NAME = 'models/gemini-2.5-flash-image'

# Initialize the model for this agent
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Error initializing image model: {e}")
    model = None

def generate_image(refined_prompt):
    """
    Calls the Gemini API to generate an image and saves it to a file.
    Returns the filename or an error message.
    """
    if not model:
        return "Error: Image worker model is not initialized."

    print(f"\n🚀 Sending to image worker...")
    print(f"   Final Prompt: \"{refined_prompt}\"")
    print("-" * 20)
    
    try:
        # Tell the model we expect an IMAGE response
        generation_config = {"responseModalities": ['IMAGE']}
        
        # Generate the content
        response = model.generate_content(
            refined_prompt, 
            generation_config=generation_config
        )
        
        # Find the image data in the response
        image_data = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_data = part.inline_data
                break
        
        if not image_data:
            return "Error: No image data returned from API."

        # Get the raw image bytes
        image_bytes = image_data.data
        
        # Create a unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        
        # Save the image bytes to the file
        path = pathlib.Path(filename)
        path.write_bytes(image_bytes)
        
        print("-" * 20)
        # Return the SUCCESS message with the new filename
        return f"✅ Success! Image saved to: {filename}"

    except Exception as e:
        print(f"Error during image generation: {e}")
        return f"Error: {e}"