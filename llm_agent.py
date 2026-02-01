import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_doc(code_chunk):
    prompt = f"""
You are a senior technical writer.

Explain this code clearly:
- Purpose
- Inputs
- Outputs
- Example usage

Code:
{code_chunk}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text, {"model": "gemini-2.5-flash"}
