from openai import OpenAI
import os
import re
import subprocess
import sys

# Fetch API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Set up OpenAI client that will be used to make API requests
client = OpenAI(api_key=api_key)

# Initial message to give to AI client to set context
messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]

# Gets specifications on OS to give AI additional context, such as OS, host, kernel, terminal, etc
def get_neofetch_output():
    try:
        # Run the neofetch command and capture its output
        output = subprocess.check_output(['neofetch', '--stdout']).decode('utf-8')
        
        # Use regular expression to remove ANSI escape codes
        clean_output = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', output)
    except Exception as e:
        print(f"Error running neofetch: {e}")
        clean_output = "Neofetch could not be run."
    return clean_output


# Gets terminal history based on the shell I use to give AI additional context
def get_terminal_history():
    history_file = os.path.expanduser("~/.local/share/fish/fish_history")
    try:
        with open(history_file, "r") as file:
            history = file.readlines()
            # Fish history format: lines starting with '- cmd: ' are actual commands
            commands = [line.strip()[6:] for line in history if line.startswith('- cmd: ')]
    except Exception as e:
        print(f"Error reading history file: {e}")
        commands = []
    return commands

# Calls openAI API with user prompt, terminal history and system sepcifications and returns response
def ask_openai(prompt, terminal_history, system_info):
    # Combine terminal history, system information, and the user's prompt
    full_prompt = f"Here is my recent terminal history: {', '.join(terminal_history[-10:])}\n\n" \
                  f"My system specifications: {system_info}\n\n" \
                  f"Question: {prompt}"

    if full_prompt:
        messages.append(
            {"role": "user", "content": full_prompt},
        )
        chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

# First argument is archero, second argument is user's query
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archero <your query>")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    context = get_terminal_history()
    system_info = get_neofetch_output()
    answer = ask_openai(prompt, context, system_info)
    print(f"OpenAI: {answer}")
