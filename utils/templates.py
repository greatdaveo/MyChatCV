
# To style the CV content into an A4 HTML Doc
def build_cv_html(name: str, email: str, content: str) -> str:
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
