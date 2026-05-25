import os
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
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            # Store the generated summary back into the item dict
            summarized_item = item.copy()
            summarized_item['summary'] = response.text.strip()
            summaries.append(summarized_item)
            print(f"Successfully summarized: {item['title']}")
        except Exception as e:
            print(f"Error summarizing {item['title']}: {e}")
            
    return summaries
