import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_reviewer(code: str, language: str, focus: str = None) -> str:
    focus_note = f"Pay special attention to: {focus}." if focus else ""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""You are an expert {language} code reviewer. 
Analyze the following code and provide structured feedback covering:
1. Bugs and logical errors
2. Security vulnerabilities
3. Code style and readability issues
4. Performance concerns
5. Best practice violations

{focus_note}

Code to review:
{code}

Format your response with clear sections and severity labels (Critical/Major/Minor)."""
        }]
    )
    return response.choices[0].message.content