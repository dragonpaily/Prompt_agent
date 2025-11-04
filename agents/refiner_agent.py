import google.generativeai as genai

# Initialize the model for this agent
try:
    refiner_model = genai.GenerativeModel('models/gemini-2.5-pro')
except Exception as e:
    print(f"Error initializing refiner model: {e}")
    refiner_model = None

def refine_prompt(original_prompt, output_type, edit_instruction=None):
    """
    Calls the LLM (Refiner Agent) to CRITICALLY rewrite or EDIT a prompt.
    
    If edit_instruction is None: Critiques and refines the original_prompt.
    If edit_instruction is provided: Applies the edit to the original_prompt.
    """
    if not refiner_model:
        print("Refiner model is not initialized. Returning original prompt.")
        return original_prompt
        
    if edit_instruction:
        # --- JOB B: We are EDITING an existing prompt ---
        print(f"\n🤖 Applying edit suggestion to prompt for {output_type}...")
        meta_prompt = f"""
        You are a master prompt editor. Your task is to take an existing, detailed prompt 
        and modify it based on a user's new instruction.

        * Do not just append the instruction.
        * Integrate the user's request logically into the prompt.
        * Return the new, complete, re-written prompt.

        THE EXISTING PROMPT IS:
        "{original_prompt}"

        THE USER'S EDIT REQUEST IS:
        "{edit_instruction}"

        Return ONLY the new, refined prompt and nothing else.
        """
    else:
        # --- JOB A: We are REFINING a vague prompt ---
        print(f"\n🤖 Critically analyzing and refining prompt for {output_type}...")
        meta_prompt = f"""
        You are an expert prompt engineer and prompt critic. 
        Your task is to first **critically analyze** the user's prompt and then
        refine it into a new, superior version.

        **Step 1: Analyze the Prompt.**
        Look for **possible problems** with the original prompt:
        - Is it too vague, simple, or ambiguous?
        - Does it lack the necessary detail for the target output type?
        - Could it be misinterpreted by the AI?
        - Is it missing key elements like style, mood, or context?

        **Step 2: Refine the Prompt.**
        Based on your analysis, rewrite the prompt to solve all identified problems.
        The new prompt must be highly detailed, descriptive, and optimized.

        The user wants to generate a: **{output_type}**

        Rules for the new, refined prompt:
        - If 'text', expand it into a clear and detailed instruction for an LLM.
        - If 'image', describe a vivid, detailed scene with style, lighting, and composition.
        - If 'video', describe a cinematic shot with subject, action, setting, mood,
          camera movement, and high-resolution details.
        
        Return ONLY the new, refined prompt and nothing else. Do not include your analysis.

        ORIGINAL PROMPT: "{original_prompt}"
        """
    
    try:
        response = refiner_model.generate_content(meta_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during refinement: {e}")
        return original_prompt # Fallback to the original prompt