import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_article(title, url):
    prompt = f"""You are an AI news summarizer. 
Summarize this AI news article in exactly 3 bullet points.
Keep each bullet point under 20 words.
Be clear and informative.

Article title: {title}
Article URL: {url}

Respond with only the 3 bullet points, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content