from groq import Groq
import groq_key
import ast

GROQ_API_KEY = groq_key.read()

def ask(prompt: str):
    client = Groq(api_key = GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    return completion
