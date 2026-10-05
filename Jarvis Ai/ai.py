import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY not found in .env")
    client = None
else:
    client = Groq(api_key=api_key)


def ask_ai(question, memory_context=""):
    
    if client is None:
        return "API key is missing."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Jarvis, a friendly AI assistant.

Give short and simple answers.
Normally answer in 1 to 3 sentences.
Do not give long explanations unless the user asks for details.
For programming questions, explain clearly and simply.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_completion_tokens=300
        )

        answer = response.choices[0].message.content

        return answer

    except Exception as e:
        print("\n========== AI ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("==============================\n")

        return "AI connection error. Check the terminal."