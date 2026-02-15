import os
import re
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def clean_text(text):
    """Remove emoji and special symbols from text"""
   
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  
        "\U0001F300-\U0001F5FF"  
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF"  
        "\U00002500-\U00002BEF"  
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
        "\ufe0f"  
        "\u3030"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(r'', text)
    
    
    text = re.sub(r'```[\w]*\n', '', text)
    text = re.sub(r'```\n?', '', text)
    
    
    text = re.sub(r'\*{3,}', '', text)  
    text = re.sub(r'#{4,}', '', text)   
    
    
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text

def generate_doc(code_chunk):
    prompt = f"""You are a professional technical documentation writer. Generate COMPREHENSIVE and DETAILED documentation for the following code. This documentation will be printed in a PDF report, so it should be substantial (minimum 5 pages worth of content).

REQUIREMENTS:
- Write in a formal, technical tone
- Be thorough and detailed - include comprehensive explanations
- Use proper markdown formatting ONLY for: headings (# ## ###), bold (**text**), code blocks (```), bullet points (* or -)
- Avoid all other markdown symbols and formatting
- DO NOT use: horizontal rules (---), tables with |, blockquotes (>), or other special markdown
- Structure the documentation with these sections:
  * # Project Overview - Detailed description of what the project does
  * ## Introduction - Purpose and context
  * ## Architecture - How the system is organized and structured
  * ## Key Components - Detailed explanation of each module/file
  * ## Features - Comprehensive list of features with explanations
  * ## Technical Details - In-depth technical information
  * ## Implementation Details - How key functionality works
  * ## Usage Examples - Multiple practical examples
  * ## Configuration - Setup and configuration details
  * ## Best Practices - Recommended practices for using this code
  * ## Troubleshooting - Common issues and solutions
  * ## Conclusion - Summary and next steps
- Include multiple code examples and explanations
- Provide at least 2-3 paragraphs for each major section
- Do not use phrases like "This code", "In this code", "Let me explain"
- Output should be detailed, professional, and suitable for complete technical documentation
- Make sure content is substantial enough for a multi-page document
- Aim for at least 5 pages worth of detailed information

Code to document:
{code_chunk}

Generate ONLY the documentation content without any preamble or introduction."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cleaned_text = clean_text(response.text)
    
    
    cleaned_text = cleaned_text.replace("In summary,", "")
    cleaned_text = cleaned_text.replace("In conclusion,", "")
    cleaned_text = cleaned_text.replace("In this code,", "")
    cleaned_text = cleaned_text.replace("This code", "The implementation")
    cleaned_text = cleaned_text.replace("Let me explain", "")
    cleaned_text = cleaned_text.replace("Here's how it works:", "")
    cleaned_text = cleaned_text.replace("As you can see,", "")
    
    
    cleaned_text = re.sub(r'(?<!\*)\*(?!\*| )', '', cleaned_text)  
    cleaned_text = re.sub(r'(?<!#)#(?!# )', '', cleaned_text)  
    
    
    cleaned_text = "\n".join(line.rstrip() for line in cleaned_text.split("\n"))
    cleaned_text = "\n".join(line for line in cleaned_text.split("\n") if line.strip())

    return cleaned_text, {"model": "gemini-2.5-flash"}
