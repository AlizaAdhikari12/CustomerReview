import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1")

def analyze_review(review_text:str):
    prompt = f"""
    Analyze this customer and return only value in JSON.

    Review :
    {review_text}

    Format:
    {{
        "sentiment":"Positive/Negative/NeutralS",
        "score" : 0.0,
        "keywords" : ["Keyword1","Keyword2"],
        "category" : "Service/Product/Support/Delay/Other",
        "summary": "short summary"
    }}
    """
    response = client.chat.completions.create(
        model ="deepseek/deepseek-chat",
        messages =[
            {"role": "system",
            "content": "You analyze customer reviews."
            },
            {"role": "user",
            "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature = 0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
        "error": "Invalid JSON",
        "raw_response": content
    }
    