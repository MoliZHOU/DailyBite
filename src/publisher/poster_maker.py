import os
from html2image import Html2Image
from jinja2 import Template
from datetime import datetime

COVER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { width: 1080px; height: 1440px; margin: 0; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; font-family: -apple-system, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
        h1 { font-size: 120px; margin-bottom: 20px; }
        h2 { font-size: 60px; font-weight: normal; color: #a8c0ff; }
        .date { font-size: 50px; margin-top: 100px; opacity: 0.8; }
    </style>
</head>
<body>
    <h1>Tech & AI Weekly</h1>
    <h2>Top Trending Repositories</h2>
    <div class="date">{{ date }}</div>
</body>
</html>
"""

CONTENT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { width: 1080px; height: 1440px; margin: 0; background: #ffffff; color: #333333; font-family: -apple-system, sans-serif; padding: 100px; box-sizing: border-box; display: flex; flex-direction: column; }
        .source { font-size: 40px; color: #2980b9; font-weight: bold; margin-bottom: 40px; text-transform: uppercase; }
        h1 { font-size: 80px; color: #2c3e50; margin-top: 0; margin-bottom: 60px; line-height: 1.2; word-break: break-all;}
        .summary { font-size: 48px; line-height: 1.6; color: #555555; white-space: pre-wrap; flex-grow: 1; overflow: hidden;}
        .footer { margin-top: auto; text-align: right; font-size: 40px; color: #bdc3c7; }
    </style>
</head>
<body>
    <div class="source">{{ item.source }}</div>
    <h1>{{ item.title }}</h1>
    <div class="summary">{{ item.summary[:600] }}{% if item.summary|length > 600 %}...{% endif %}</div>
    <div class="footer">{{ index }} / {{ total }}</div>
</body>
</html>
"""

def generate_posters(items, output_dir='posters'):
    os.makedirs(output_dir, exist_ok=True)
    
    # Chrome may not be in PATH in GH actions, so we might need custom args or paths later
    try:
        hti = Html2Image(output_path=output_dir)
    except Exception as e:
        print(f"Warning: html2image init failed. Are Chrome/Chromium installed? {e}")
        return
        
    # Generate Cover (Image 1)
    cover_html = Template(COVER_TEMPLATE).render(date=datetime.now().strftime('%Y-%m-%d'))
    try:
        hti.screenshot(html_str=cover_html, size=(1080, 1440), save_as='01_cover.png')
        print("Generated cover poster")
    except Exception as e:
        print(f"Failed to generate cover: {e}")
    
    # Generate Content (Images 2-5)
    # Take up to 4 items
    selected_items = items[:4]
    total_slides = len(selected_items) + 1
    
    for i, item in enumerate(selected_items):
        idx = i + 2
        content_html = Template(CONTENT_TEMPLATE).render(item=item, index=idx, total=total_slides)
        try:
            hti.screenshot(html_str=content_html, size=(1080, 1440), save_as=f'{idx:02d}_content.png')
            print(f"Generated content poster {idx}")
        except Exception as e:
            print(f"Failed to generate content poster {idx}: {e}")
