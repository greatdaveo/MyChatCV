import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# To generate CV Sections from parsed input data
async def generate_cv_content(parsed_data:dict)-> dict:
    name = parsed_data.get("name", "")
    experience = parsed_data.get("experience", "")
    skills = parsed_data.get("skills", "")
    companies = parsed_data.get("companies", "")
    email = parsed_data.get("email", "")

    prompt = f"""
    Create a professional CV using the content information below
    - Name: {name}
    - Email: {email}
    - Experience: {experience}
    - Companines: {companies}
    - Skills: {skills}
    
    format:
    1. Personal Summary
    2. Work Experience Description
    3. Skills Highlights    
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional CV writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        content = response.choices[0].message.content.strip()

        return {
            "name": name,
            "email":email,
            "content": content
        }
    except Exception as e:
        raise Exception(f"Error generating CV content: {str(e)}")

def parse_message(message: str)-> Dict[str, str]:
    """
    Parses structured WhatsApp message into a dictionary of fields.
    Expected format:
    "Generate my CV:
    Name: John Doe
    Email: john@example.com
    LinkedIn: linkedin.com/in/johndoe
    Experience: 5 years
    Skills: Python, FastAPI
    ..."
    """
    try:
        lines = message.split('\n')
        parsed_data = {}

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_data[key.strip().lower()] = value.strip()
        return parsed_data

    except Exception as e:
        raise ValueError(f"❌ Error Parsing Message: {str(e)}")