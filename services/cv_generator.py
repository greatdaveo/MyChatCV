import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# To generate CV Sections from parsed input data


async def generate_cv_content(parsed_data: dict) -> dict:
    name = parsed_data.get("name", "")
    experience = parsed_data.get("experience", "")
    skills = parsed_data.get("skills", "")
    companies = parsed_data.get("companies", "")
    email = parsed_data.get("email", "")
    linkedin = parsed_data.get("linkedin", "")
    phone = parsed_data.get("phone", "")
    education = parsed_data.get("education", "")
    location = parsed_data.get("location", "")

    prompt = f"""
    Create a professional, well-structured CV for {name}. Use the following information to generate a comprehensive CV that follows modern professional standards:
    PERSONAL INFORMATION:
    - Name: {name}
    - Email: {email}
    - Phone: {phone}
    - Location: {location}
    - LinkedIn: {linkedin}
    - Total Experience: {experience}

    WORK EXPERIENCE:
    {companies}

    SKILLS:
    {skills}

    EDUCATION:
    {education}

    Please create a professional CV with the following structure:

    1. **Professional Summary** (2-3 sentences highlighting key achievements and career focus)
    2. **Core Competencies** (6-8 key skills organized by category)
    3. **Professional Experience** (detailed work history with achievements, responsibilities, and quantifiable results)
    4. **Education & Certifications** (if applicable)
    5. **Technical Skills** (organized by proficiency level)

    Guidelines:
    - Use action verbs and quantifiable achievements
    - Focus on recent and relevant experience
    - Include specific metrics and results where possible
    - Use professional language and industry-standard formatting
    - Ensure all content is factual and professional
    - Make it ATS-friendly with clear section headers
    - Keep it concise but comprehensive (1-2 pages when formatted)

    Format the output with clear section headers using **bold** text and proper spacing.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert CV writer with 15 + years of experience in HR and recruitment. You specialize in creating professional, ATS-friendly CVs that help candidates stand out. Always focus on achievements, use quantifiable results, and structure content for maximum impact. Use professional language and ensure all content is factual and well-organized."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.3,
            max_tokens=3000
        )

        content = response.choices[0].message.content

        # print(content)

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "content": content
        }
    except Exception as e:
        raise Exception(f"Error generating CV content: {str(e)}")


def parse_message(message: str) -> Dict[str, str]:
    one_line = " ".join(message.splitlines()).strip()

    # To try structured format first (existing format)
    structured_pattern = re.compile(
        r"Generate\s+my\s+CV:\s*"
        r"Name:\s*(?P<name>.*?)\s+"
        r"Email:\s*(?P<email>.*?)\s+"
        r"LinkedIn:\s*(?P<linkedin>.*?)\s+"
        r"Experience:\s*(?P<experience>.*?)\s+"
        r"Companies:\s*(?P<companies>.*?)\s+"
        r"Skills:\s*(?P<skills>.*)$",
        re.IGNORECASE
    )

    match = structured_pattern.search(one_line)
    if match:
        return {
            "name": match.group("name").strip(),
            "email": match.group("email").strip(),
            "linkedin": match.group("linkedin").strip(),
            "experience": match.group("experience").strip(),
            "companies": match.group("companies").strip(),
            "skills": match.group("skills").strip(),
            "phone": "",
            "location": "",
            "education": ""
        }

    # To tru conversational format
    conversational_pattern = re.compile(
        r"(?i)(?:my name is|i'm|i am)\s+(?P<name>[^,]+)(?:,|\.|\s|$)"
    )

    name_match = conversational_pattern.search(one_line)
    if name_match:
        # To extract basic info from conversational message
        name = name_match.group('name').strip()

        # To extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, one_line)
        email = email_match.group(0) if email_match else ""

        # To extract phone number
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        phone_match = re.search(phone_pattern, one_line)
        phone = phone_match.group(1) if phone_match else ""

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": "",
            "experience": "",
            "companies": "",
            "skills": "",
            "location": "",
            "education": ""
        }

    raise ValueError(
        "Message format not recognized. Please use the structured format or provide your name clearly.",
    )

# To extract CV data from a conversation flow


def extract_cv_data_from_conversation(messages: List[str]) -> Dict[str, str]:
    extracted_data = {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "experience": "",
        "companies": "",
        "skills": "",
        "location": "",
        "education": ""
    }

    for message in messages:
        if not extracted_data["name"]:
            name_pattern = r"(?i)(?:my name is|i'm|i am)\s+([^,\.]+)"
            name_match = re.search(name_pattern, message)
            if name_match:
                extracted_data["name"] = name_match.group(1).strip()

        if not extracted_data["email"]:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_match = re.search(email_pattern, message)
            if email_match:
                extracted_data["email"] = email_match.group(0)

        if not extracted_data["phone"]:
            phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
            phone_match = re.search(phone_pattern, message)
            if phone_match:
                extracted_data["phone"] = phone_match.group(1)

        if not extracted_data["experience"]:
            exp_pattern = r"(?i)(?:experience|worked|have been working)\s+(?:for\s+)?(\d+\s+(?:years?|yrs?))"
            exp_match = re.search(exp_pattern, message)
            if exp_match:
                extracted_data["experience"] = exp_match.group(1)

        if not extracted_data["skills"]:
            skills_pattern = r"(?i)(?:skills?|technologies?|tools?)\s*[:\-]?\s*([^\.]+)"
            skills_match = re.search(skills_pattern, message)
            if skills_match:
                extracted_data["skills"] = skills_match.group(1).strip()

    return extracted_data
