import os
import re
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def clean_text(text):
    """Remove emoji and special symbols from text"""
    # Remove emoji characters
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(r'', text)
    return text

def generate_doc(code_chunk):
    prompt = f"""You are a professional technical documentation writer. Generate comprehensive, concise, and professional documentation for the following code.

REQUIREMENTS:
- Write in a formal, technical tone
- Be concise and clear
- Use proper markdown formatting
- Avoid casual language or filler text
- Structure the documentation logically
- Include code examples where relevant
- Do not use phrases like "This code", "In this code", "Let me explain"
- Focus on: Overview, Key Features, Architecture, Usage, Configuration
- Output should be suitable for professional documentation

Code to document:
{code_chunk}

Generate ONLY the documentation content without any preamble or introduction."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cleaned_text = clean_text(response.text)
    
    # Remove common AI-generated phrases
    cleaned_text = cleaned_text.replace("In summary,", "")
    cleaned_text = cleaned_text.replace("In conclusion,", "")
    cleaned_text = cleaned_text.replace("In this code,", "")
    cleaned_text = cleaned_text.replace("This code", "The implementation")
    cleaned_text = cleaned_text.replace("Let me explain", "")
    cleaned_text = cleaned_text.replace("Here's how it works:", "")
    cleaned_text = cleaned_text.replace("As you can see,", "")
    
    # Clean up extra whitespace
    cleaned_text = "\n".join(line.rstrip() for line in cleaned_text.split("\n"))
    cleaned_text = "\n".join(line for line in cleaned_text.split("\n") if line.strip())

    return cleaned_text, {"model": "gemini-2.5-flash"}
