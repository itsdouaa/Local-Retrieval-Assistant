from groq import Groq
import subprocess

def read_key():
    try:
        result = subprocess.run(
            ["cat", "/etc/groq_API.txt"],
            check=True,
            text=True,
            capture_output=True
        )
        key = result.stdout.strip()
        return key
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Impossible de lire la clé API") from e

GROQ_API_KEY = read_key()

def response(messages):
    client = Groq(api_key = GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=4096,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    return completion
