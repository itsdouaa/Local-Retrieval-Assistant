import os

def read():
    """
    Read the Groq API key from groq_API.txt in the project directory.
    """
    # Get the path to groq_API.txt in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_key_path = os.path.join(current_dir, "groq_API.txt")
    
    if not os.path.exists(api_key_path):
        raise RuntimeError(
            "Groq API key not found. Please create groq_API.txt in the project directory.\n"
            "The file should contain only your API key."
        )
    
    try:
        with open(api_key_path, 'r', encoding='utf-8') as f:
            api_key = f.read().strip()
            if not api_key:
                raise RuntimeError("API key file is empty.")
            return api_key
    except Exception as e:
        raise RuntimeError(f"Error reading API key: {e}")