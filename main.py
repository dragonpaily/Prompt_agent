# --- Import local modules ---
from config import load_api_key
from agents.refiner_agent import refine_prompt
from agents.text_agent import generate_text
from agents.image_agent import generate_image
from agents.video_agent import generate_video

def main_loop():
    """
    The main controller that manages the user interaction and agent calls.
    """
    print("Welcome to the Iterative Prompt Refinement Agent")
    print("You can generate 'text', 'image', or 'video'. Type 'quit' to exit.")

    # A dictionary to map user's choice to the correct agent function
    worker_agents = {
        'text': generate_text,
        'image': generate_image,
        'video': generate_video
    }

    while True:
        # --- Step 1: Get User Input ---
        original_prompt = input("\nEnter your simple prompt: ")
        if original_prompt.lower() == 'quit':
            break

        while True:
            output_type = input("What do you want to generate? (text/image/video): ").lower()
            if output_type in worker_agents:
                break
            elif output_type == 'quit':
                return
            else:
                print("Invalid type. Please enter 'text', 'image', or 'video'.")
        
        # --- Step 2: First Refinement ---
        current_prompt = refine_prompt(original_prompt, output_type)
        
        # --- Step 3: The Iterative Refinement Loop ---
        while True:
            print(f"\n✨ Refined Prompt:\n{current_prompt}")
            
            choice = input(
                "\nChoose an action: [G]enerate, [R]efine again, [E]dit, [S]tart over: "
            ).lower()

            if choice == 'g':
                # --- Step 4: Execution ---
                print("\n⏳ Generating output, please wait...")
                
                # Call the correct worker function and store its RETURN value
                result = worker_agents[output_type](current_prompt)
                
                # Print the final result (either the story or the filename)
                print(result)
                
                print("-" * 20)
                break # Break inner loop to start a new project
                
            elif choice == 'r':
                # Run the refinement again on the *current* prompt
                current_prompt = refine_prompt(current_prompt, output_type)
                
            elif choice == 'e':
                # Get the user's edit instruction
                print("\nWhat change would you like to make?")
                edit_instruction = input("Edit Suggestion: ")

                # Call the refiner agent, passing the *current prompt* and the *new edit*
                current_prompt = refine_prompt(
                    original_prompt=current_prompt, 
                    output_type=output_type, 
                    edit_instruction=edit_instruction
                )
                
            elif choice == 's':
                break # Break inner loop to start a new project
            
            else:
                print("Invalid choice. Please try again.")

    print("Goodbye!")

# --- Run the application ---
if __name__ == "__main__":
    # First, try to load and configure the API key
    if load_api_key():
        # If successful, run the main application loop
        main_loop()
    else:
        print("Application cannot start without a valid API key.")