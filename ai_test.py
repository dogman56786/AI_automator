import os
import subprocess
import sys
import ollama  # Make sure to use this in your section!

def control_app(action, app_name):
    """This function handles the heavy lifting of opening and closing apps on Windows."""
    app_name_lower = app_name.lower()
    
    # Mapping common names to their actual executable files
    app_commands = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "terminal": "cmd.exe",
        "browser": "zen.exe"  # Change this to whatever browser you use (e.g., chrome.exe, zen.exe)
    }
    
    exe = app_commands.get(app_name_lower, app_name_lower + ".exe")

    if action == "open":
        print(f"🚀 Attempting to open {app_name}...")
        try:
            subprocess.Popen(exe, shell=True)
            return f"Successfully opened {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}. Error: {e}"
            
    elif action == "close":
        print(f"🛑 Attempting to close {app_name}...")
        # taskkill forces a program to close on Windows
        result = os.system(f"taskkill /f /im {exe} >nul 2>&1")
        if result == 0:
            return f"Successfully closed {app_name}."
        else:
            return f"Could not close {app_name}. It might not be running."

# =====================================================================
# YOUR TURN: Write the AI logic below!
# =====================================================================

print("AI OS Agent Active. Type what you want to do (e.g., 'open notepad' or 'close calculator')")
user_input = input("You: ")

# 1. Write your system prompt instructing nemotron-3-super:cloud to ONLY output 
#    the exact action and app name separated by a comma (e.g., "open,notepad")
# 2. Call response = ollama.chat(...) using your model
# 3. Extract the clean text response from the model

 # Running the cloud model with specific system rules
response = ollama.chat(
    model='nemotron-3-super:cloud', 
    messages=[
        {
            'role': 'system',
            'content': (
                "You are a strict OS automation parser. Your job is to read the user's intent "
                "and extract the action (open or close) and the application name. "
                "You must ONLY respond in this exact format: action,app\n"
                "Examples:\n"
                "User: 'launch notepad' -> open,notepad\n"
                "User: 'kill the calculator' -> close,calculator\n"
                "Do NOT include code blocks, markdown, or full sentences. Just raw text."
                "Do not ever open a browser or any other application unless explicitly instructed by the user. "
            )
        },
        {
            'role': 'user',
            'content': user_input
        }
    ]
)

# Extract the clean string from the model response
ai_decision = response['message']['content'].strip()
# =====================================================================
# AFTER YOUR CODE RUNS: This part takes your AI's decision and runs it
# =====================================================================

# Let's assume you save the AI's response text into a variable called 'ai_decision'
# Example layout: ai_decision = response['message']['content'].strip()

try:
    # Splitting the "open,notepad" response into two pieces
    action, app = ai_decision.split(",")
    action = action.strip().lower()
    app = app.strip().lower()
    
    # Run the automation
    status = control_app(action, app)
    print(f"Agent Status: {status}")
except Exception as e:
    print(f"Could not parse the AI's response. Make sure it output exactly 'action,app'.")
    print(f"AI actually said: '{ai_decision}'")