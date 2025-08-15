from fastapi import APIRouter, Form, Response
from fastapi.responses import Response
from services.cv_generator import parse_message, generate_cv_content, extract_cv_data_from_conversation
from utils.cloudinary_upload import upload_file_to_cloudinary
from utils.pdf import create_pdf_file
from utils.generate_doc import create_docx_file
from twilio.twiml.messaging_response import MessagingResponse
import re


router = APIRouter()

# To store user storage
user_sessions = {}

# To extract years of experience from whatsapp message


def extract_years_of_experience(text: str) -> int:
    t = text.lower()
    # e.g. "I have 3 years", "3yrs", "3+ years"
    m = re.search(r'(\d+)\s*\+?\s*(?:years?|yrs?)', t)
    if m:
        return int(m.group(1))
    # e.g. "experience: 3"
    m = re.search(r'experience\s*[:\-]?\s*(\d+)', t)
    if m:
        return int(m.group(1))
    return 0


def build_welcome_message() -> str:
    return (
        "👋 *Welcome to MyChatCV - Your AI CV Assistant!*\n\n"
        "I'll help you create a professional CV in just a few minutes. You can:\n\n"
        "📝 *Option 1: Quick Format*\n"
        "Send your details in this format:\n"
        "```\n"
        "Generate my CV:\n"
        "Name: Your Full Name\n"
        "Email: your.email@example.com\n"
        "Phone: +1234567890\n"
        "Experience: 5 years\n"
        "Companies: Company1: Role (2020-2023), Company2: Role (2018-2020)\n"
        "Skills: Python, JavaScript, React, AWS\n"
        "```\n\n"
        "💬 *Option 2: Chat Mode*\n"
        "Just tell me your name and I'll guide you through the process!\n\n"
        "Which option would you prefer?"
    )


def build_help_message() -> str:
    return (
        "�� *Need Help?*\n\n"
        "Here are some examples:\n\n"
        "*Quick Format:*\n"
        "```\n"
        "Generate my CV:\n"
        "Name: John Doe\n"
        "Email: john@example.com\n"
        "Phone: +1234567890\n"
        "Experience: 3 years\n"
        "Companies: TechCorp: Role (2021-2023)\n"
        "Skills: Python, React, AWS\n"
        "```\n\n"
        "*Chat Mode:*\n"
        "Just say: \"Hi, my name is John Doe\"\n\n"
        "Need more help? Type 'help' anytime!"
    )

# To handle cv conversation flow


async def build_conversation_flow(user_id: str, message: str) -> str:
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "step": "name",
            "data": {},
            "messages": []
        }

    session = user_sessions[user_id]
    session["messages"].append(message.lower())

    # To extract basic info from the message
    extracted_data = extract_cv_data_from_conversation([message])

    if session["step"] == "name":
        if extracted_data["name"]:
            session["data"]["name"] = extracted_data["name"]
            session["step"] = "email"
            return (
                f"Great! Nice to meet you, {extracted_data['name']}! 👋\n\n"
                "Now, please share your email address so I can include it in your CV."
            )
        else:
            return (
                "I didn't catch your name. Could you please tell me your full name?\n"
                "For example: \"My name is John Doe\""
            )

    elif session["step"] == 'email':
        if extracted_data["email"]:
            session["data"]["email"] = extracted_data["email"]
            session["step"] = "experience"
            return (
                f"Perfect! 📧\n\n"
                "How many years of professional experience do you have?\n"
                "For example: \"I have 5 years of experience\" or \"3 years\""
            )
        else:
            return (
                "I need your email address for your CV. Please share it with me.\n"
                "For example: \"My email is john@example.com\""
            )

    elif session["step"] == "experience":
        years = extracted_data.get("experience")
        if not years:
            parsed = extract_years_of_experience(message)
            if parsed is not None:
                years = parsed

        if years:
            years_str = f"{years} years" if isinstance(
                years, int) else str(years).strip()
            session["data"]["experience"] = years_str
            session["step"] = "companies"
            return (
                f"Excellent! {extracted_data['experience']} of experience. 📈\n\n"
                "Now, tell me about your work experience. You can say something like:\n"
                "\"I worked at Google as a Software Engineer from 2020 to 2023, and before that at Microsoft as a Developer from 2018 to 2020\""
            )
        else:
            return (
                "I need to know your years of experience. Please tell me how many years you've been working.\n"
                "For example: \"I have 5 years of experience\""
            )

    elif session["step"] == "companies":
        # Extract company information from the message
        session["data"]["companies"] = message
        session["step"] = "skills"
        return (
            "Great! Now tell me about your skills and technologies.\n"
            "For example: \"I know Python, JavaScript, React, AWS, and Docker\""
        )

    elif session["step"] == "skills":
        session["data"]["skills"] = message
        session["step"] = "generate"

        try:
            cv = await generate_cv_content(session["data"])
            name = cv["name"]
            email = cv["email"]
            content = cv["content"]

            # To generate files
            print("Generating PDF...")
            pdf_path = create_pdf_file(name, email, content,
                                       session["data"].get("phone", ""),
                                       session["data"].get("location", ""),
                                       session["data"].get("linkedin", ""))
            print(f"PDF generated at: {pdf_path}")

            print("Generating DOCX...")
            docx_path = create_docx_file(name, email, content,
                                         session["data"].get("phone", ""),
                                         session["data"].get("location", ""),
                                         session["data"].get("linkedin", ""))
            print(f"DOCX generated at: {docx_path}")

            # To upload files
            print("Uploading to Cloudinary...")
            pdf_url = upload_file_to_cloudinary(pdf_path)
            print(f"PDF uploaded: {pdf_url}")
            docx_url = upload_file_to_cloudinary(docx_path)

            print(f"PDF URL: {pdf_url}")
            print(f"DOCX URL: {docx_url}")

            print(f"Skills received: {message}")
            print(f"Session data: {session['data']}")
            print(f"PDF Path: {pdf_path}")
            print(f"DOCX Path: {docx_path}")

            # To clean up session
            del user_sessions[user_id]

            return (
                f"🎉 *Congratulations, {name}! Your CV is ready!*\n\n"
                f"📄 *PDF Version:* {pdf_url}\n"
                f"📝 *Word Version:* {docx_url}\n\n"
                "Your CV has been professionally formatted and is ready to use!\n\n"
                "💡 *Tips:*\n"
                "• Download both versions\n"
                "• Customize if needed\n"
                "• Use for job applications\n\n"
                "Thanks for using MyChatCV! 🚀"
            )

        except Exception as e:
            print(f"build_conversation_flow Error: {str(e)}")

            return (
                f"❌ Sorry, I encountered an error while generating your CV:\n{str(e)}\n\n"
                "Please try again or use the quick format option."
            )


# To receive form-encoded data from Twilio WhatsApp Webhook
@router.post("/twilio/webhook")
async def twilio_webhook(
        body: str = Form(..., alias="Body"),  # The user's message
        # The sender's WhatsApp Number
        from_number: str = Form(..., alias="From")
):
    def twiml_response(text: str) -> Response:
        resp = MessagingResponse()
        resp.message(text)
        return Response(content=str(resp), media_type="application/xml")

    # To log incoming messages
    # print("---- Received WhatsApp Payload -------")
    # print("From: ", from_number)
    # print("Body: ", body)
    # print("-------------------------------------------")

    # To extract user ID from the phone number
    user_id = from_number.replace("whatsapp:", "")

    # To handle special commands
    if body.lower() in ["help", "h", "?"]:
        return twiml_response(build_help_message())

    if body.lower() in ["restart", "reset", "new"]:
        if user_id in user_sessions:
            del user_sessions[user_id]
        return twiml_response(
            "⚠️ Session reset! Let's start fresh.\n\n" + build_welcome_message()
        )

    # To check if the user is in conversation mode
    if user_id in user_sessions:
        return twiml_response(await build_conversation_flow(user_id, body))

    # To check for structured format
    if body.lower().startswith("generate my cv:"):
        try:
            parsed_data = parse_message(body)
        except ValueError:
            return twiml_response(
                "⚠️ I couldn't parse your request. Please check the format.\n\n" + build_help_message()
            )

        # To validate required fields
        required_keys = ["name", "email"]
        missing_keys = [
            key for key in required_keys if key not in parsed_data or not parsed_data[key].strip()]
        if missing_keys:
            return twiml_response(
                f"⚠️ Missing required field(s): {', '.join(missing_keys)}.\n"
                "Please include these and resend in the correct format."
            )

        # To geerate the CV
        try:
            # To parse the WhatsApp text and generate content
            cv = await generate_cv_content(parsed_data)
            name, email, content = cv["name"], cv["email"], cv["content"]

            # To generate the files and upload to Cloudinary
            pdf_path = create_pdf_file(name, email, content,
                                       parsed_data.get("phone", ""),
                                       parsed_data.get("location", ""),
                                       parsed_data.get("linkedin", ""))
            docx_path = create_docx_file(name, email, content,
                                         parsed_data.get("phone", ""),
                                         parsed_data.get("location", ""),
                                         parsed_data.get("linkedin", ""))

            pdf_url = upload_file_to_cloudinary(pdf_path)
            docx_url = upload_file_to_cloudinary(docx_path)

            # To set up the WhatsApp response to be sent to the user
            return twiml_response(
                f"✅ *Hi {name}, your CV is ready!*\n\n"
                f"📄 *PDF Version:* {pdf_url}\n"
                f"📝 *Word Version:* {docx_url}\n\n"
                "Your professionally formatted CV is ready to use!\n\n"
                "Thanks for using MyChatCV! 🚀"
            )

        except Exception as e:
            return twiml_response(
                f"❌ Sorry, I encountered an error while generating your CV:\n{str(e)}\n\n"
                "Please try again or type 'help' for assistance."
            )

    if any(phrase in body.lower() for phrase in ["my name is", "i'm", "i am", "hi", "hello", "hey"]):
        return twiml_response(await build_conversation_flow(user_id, body))

    # For default response
    return twiml_response(build_welcome_message())
