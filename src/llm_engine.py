import os
import time
from google import genai

def init_gemini():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing!")
    return genai.Client(api_key=api_key)

def summarize_items(items, language='zh'):
    if not items:
        return []
    
    client = init_gemini()
    
    summaries = []
    for item in items:
        lang_prompt = "Please write the output ENTIRELY in Chinese (Simplified)." if language == 'zh' else "Please write the output ENTIRELY in English."
        
        prompt = f"""
You are a top-tier tech journalist writing an engaging, story-telling style report about a new trending tech project.
        
Project Name: {item['title']}
Short Description: {item['description']}
        
Your task:
Write a short, engaging story (2-3 paragraphs) about this project.
Do NOT use bullet points. Make it flow naturally like a news report.
Focus on:
1. What is this trending technology?
2. How is it done or how to use it briefly?
3. What are the key application scenarios?
4. Who is the target audience?

{lang_prompt}
Make the tone enthusiastic, professional yet highly readable and accessible.
"""
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                summarized_item = item.copy()
                summarized_item['summary'] = response.text.strip()
                summaries.append(summarized_item)
                print(f"Successfully summarized: {item['title']}")
                time.sleep(15)  # 避免触发免费层频率限制
                break
            except Exception as e:
                if '429' in str(e):
                    print(f"Rate limited (429) for {item['title']}. Sleeping for 30s before retry {attempt+1}/{max_retries}...")
                    time.sleep(30)
                else:
                    print(f"Error summarizing {item['title']}: {e}")
                    break
            
    return summaries
