
from typing import Dict

def generate_cv_content():
    return

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