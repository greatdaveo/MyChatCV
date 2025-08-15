import re

# To style the CV content into an A4 HTML Doc


def build_cv_html(name: str, email: str, content: str, phone: str = "", location: str = "", linkedin: str = "") -> str:
    formatted_content = process_cv_content(content)

    # To build contact info
    contact_info = []
    if email:
        contact_info.append(f'<span class="contact-item">📧 {email}</span>')
    if phone:
        contact_info.append(f'<span class="contact-item">📱 {phone}</span>')
    if location:
        contact_info.append(f'<span class="contact-item">📍 {location}</span>')
    if linkedin:
        contact_info.append(f'<span class="contact-item">💼 {linkedin}</span>')

    contact_html = '<div class="contact-info">' + \
        ' • '.join(contact_info) + '</div>' if contact_info else ''

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{name} - Professional CV</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #2d3748;
                background: #ffffff;
                font-size: 14px;
            }}
            
            .cv-container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 40px;
                background: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 3px solid #3182ce;
            }}
            
            .name {{
                font-size: 2.5em;
                font-weight: 700;
                color: #1a202c;
                margin-bottom: 10px;
                letter-spacing: -0.5px;
            }}
            
            .title {{
                font-size: 1.2em;
                color: #4a5568;
                font-weight: 500;
                margin-bottom: 15px;
            }}
            
            .contact-info {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 15px;
                font-size: 0.9em;
                color: #4a5568;
            }}
            
            .contact-item {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            
             .section {{
                margin-bottom: 25px;
            }}
            
            .section-title {{
                font-size: 1.3em;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 2px solid #e2e8f0;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .content {{
                color: #4a5568;
                line-height: 1.7;
            }}
            
            .highlight {{
                background: #ebf8ff;
                padding: 2px 6px;
                border-radius: 3px;
                color: #2b6cb0;
                font-weight: 500;
            }}
            
            .achievement {{
                background: #f0fff4;
                padding: 8px 12px;
                border-radius: 4px;
                border-left: 3px solid #38a169;
                margin: 8px 0;
            }}
                        
           @media print {{
                .cv-container {{
                    box-shadow: none;
                    padding: 20px;
                }}
                
                body {{
                    font-size: 12px;
                }}
                
                .name {{
                    font-size: 2em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="cv-container">
            <div class="header">
                <h1 class="name">{name}</h1>
                
                <div class="title">Professional CV</div>
                {contact_html}
            </div>
            
            <div class="content">
                {formatted_content}
            </div>
        </div>
    </body>
    </html>
    """
# To process the CV content to convert markdown-style formatting to HTML, and enhance visual presentation


def process_cv_content(content: str) -> str:
    sections = content.split('\n\n')
    processed_sections = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # To check if this is a section header, starts with **
        if section.startswith('**') and section.endswith('**'):
            section_title = section.strip('*').strip()
            processed_sections.append(
                f'<div class="section"><h2 class="section-title">{section_title}</h2>')
        else:
            # To process regular content
            processed_content = process_section_content(section)
            processed_sections.append(processed_content)


# To process individual section content to enhance formatting
def process_section_content(content: str) -> str:
    # To convert line breaks to HTML
    content = content.replace('\n', '<br>')
    # To highlight key achievements, (lines starting with - or dot)
    content = re.sub(
        r'^[•\-]\s*(.+)$', r'<div class="achievement">✓ \1</div>', content, flags=re.MULTILINE)
    # To highlight important keywords
    important_keywords = ['achieved', 'increased', 'decreased',
                          'improved', 'developed', 'managed', 'led', 'created']
    for keyword in important_keywords:
        content = re.sub(
            rf'\b{keyword}\b',
            rf'<span class="highlight">{keyword}</span>',
            content,
            flags=re.IGNORECASE
        )

    return f'<div class="content">{content}</div>'


def build_simple_cv_html(name: str, email: str, content: str) -> str:
    """
    Simple CV template for fallback or basic formatting.
    """
    formatted_content = content.replace("\n", "<br />")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{name} - CV</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 40px;
                background: #fff;
                color: #333;
                line-height: 1.6;
            }}
            h1, h2, h3 {{
                color: #0E7490;
            }}
            hr {{
                margin: 20px 0;
            }}
            .section-title {{
                font-size: 1.2em;
                margin-top: 30px;
                border-bottom: 2px solid #eee;
                padding-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>{name}</h1>
        <p><strong>Email:</strong> {email}</p>
        <hr />
        {formatted_content}
    </body>
    </html>
    """
