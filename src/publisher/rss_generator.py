from feedgen.feed import FeedGenerator
import os
from datetime import datetime, timezone

def generate_rss(items, output_file='feed.xml', language='zh'):
    fg = FeedGenerator()
    fg.id(f'https://github.com/molly/ai_news_summary_{language}')
    fg.title('Tech & AI Daily Brief' if language == 'en' else '科技与AI每日速递')
    fg.author({'name': 'Antigravity AI'})
    fg.link(href='https://github.com/molly/ai_news_summary', rel='alternate')
    fg.description('Daily AI and Tech News Summarized by Gemini')
    fg.language(language)
    
    # Add items in reverse order so newest is at the top
    for item in reversed(items):
        fe = fg.add_entry()
        fe.id(item['id'])
        fe.title(item['title'])
        fe.link(href=item['url'])
        
        # Use generated summary if available, otherwise fallback to description
        content = item.get('summary', item.get('description', ''))
        # Convert newlines to <br> for better RSS rendering
        content_html = content.replace('\n', '<br>')
        
        fe.description(content_html)
        
        # We try to use the item's saved timestamp, or default to now
        timestamp = item.get('timestamp')
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
        else:
            dt = datetime.now(timezone.utc)
            
        fe.pubDate(dt)
        
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    fg.rss_file(output_file)
    print(f"Generated RSS feed at {output_file}")
