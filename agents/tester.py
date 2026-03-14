import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_tester(code: str, language: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""You are an expert {language} testing engineer.
Generate comprehensive test cases for the following code.
Include:
1. Happy path tests
2. Edge cases
3. Error/exception handling tests
4. Boundary conditions

Write actual runnable test code using the appropriate test framework
(pytest for Python, Jest for JS, etc.)

Code to test:
{code}
"""
        }]
    )
    return response.choices[0].message.content