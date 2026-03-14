import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_improver(code: str, language: str, review_feedback: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""You are an expert {language} developer.
You have been given code and a review of its issues.
Rewrite the code addressing ALL issues found in the review.

Original code:
{code}

Review feedback:
{review_feedback}

Provide:
1. The fully improved, production-ready code
2. A brief changelog of what you fixed and why"""
        }]
    )
    return response.choices[0].message.content