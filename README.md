# MyChatCV - WhatsApp AI CV Generator

MyChatCV is a WhatsApp bot that helps users create professional CVs using AI. It generates high-quality, well-structured CVs without the stress of manual formatting.

## Features

### Enhanced CV Generation

* AI-powered content generation using OpenAI GPT-4.
* Professional, ATS-friendly CV templates.
* Export to PDF and Word (.docx) formats.
* Supports both structured and conversational input formats.

### User-Friendly Workflow

* Conversational mode for natural chat-based CV creation.
* Quick format option for structured input.
* Step-by-step guidance through the CV creation process.
* Clear and informative error messages.

### WhatsApp Integration

* Integrated with Twilio’s WhatsApp API.
* Session management to track user progress.
* Direct download links for generated files via Cloudinary.

---

## Setup Instructions

### Prerequisites

* Python 3.8 or higher
* Twilio account with WhatsApp Business API access
* OpenAI API key
* Cloudinary account for file hosting
* pdfkit and wkhtmltopdf for HTML-to-PDF generation

---

### 1. Clone the repository

```bash
git clone https://github.com/greatdaveo/MyChatCV
cd MyChatCV
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install wkhtmltopdf

```bash
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# Windows
# Download from https://wkhtmltopdf.org/downloads.html
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
WHATSAPP_FROM=whatsapp:+14155238886
```

---

## Running the Application

### Local Development

```bash
uvicorn app.main:app --reload
```

The server will run at:

```
http://127.0.0.1:8000
```

---

## Twilio Configuration

### 1. WhatsApp Sandbox Setup

* Go to Twilio Console → Messaging → Try it Out → WhatsApp Sandbox
* Follow the instructions to connect your WhatsApp number.

### 2. Webhook URL

* Set the **Webhook URL** in Twilio to:

```
https://<your-ngrok-domain>/twilio/webhook
```

* Method: POST
* Event: When a message comes in

### 3. Local Testing with ngrok

You can test locally by exposing your FastAPI server with ngrok:

```bash
ngrok http 8000
```

* Copy the ngrok HTTPS URL and set it as the Twilio webhook.

---

## Usage Examples

### Quick Format (Structured Input)

Send a WhatsApp message in this exact format:

```
Generate my CV:
Name: John Doe
Email: john@example.com
LinkedIn: linkedin.com/in/johndoe
Experience: 5 years
Companies: Google: Frontend Engineer (2018-2023)
Skills: Python, JavaScript, AWS, Docker
```

### Conversational Mode

* The bot will guide you step-by-step, asking questions about your name, email, work experience, and skills.
* At the end, you’ll receive direct download links for your CV in PDF and DOCX formats.

---

## 👨‍💻 Developed By
> Olowomeye David [GitHub](https://github.com/greatdaveo) [LinkedIn](https://linkedin.com/in/greatdaveo)

---