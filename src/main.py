import yaml
import os
from datetime import datetime
import json
import sys

# Add src to python path for relative imports if run directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adapters.github_trend import fetch_trending_repos
from deduplicator import filter_new_items, mark_as_processed
from llm_engine import summarize_items
from publisher.rss_generator import generate_rss
from publisher.web_builder import build_webpage

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    settings = load_config('config/settings.yaml')['settings']
    sources = load_config('config/sources.yaml')['sources']
    
    all_new_items = []
    
    if sources.get('github_trending', {}).get('enabled'):
        print("Fetching GitHub Trending...")
        limit = sources['github_trending'].get('limit', 10)
        repos = fetch_trending_repos()[:limit]
        all_new_items.extend(repos)
    
    # Deduplicate
    new_items = filter_new_items(all_new_items)
    print(f"Found {len(new_items)} new items after deduplication.")
    
    if not new_items:
        print("No new items to process today. Exiting.")
        return
    
    # Summarize
    language = settings.get('language', 'zh')
    print(f"Summarizing {len(new_items)} items in {language}...")
    summarized_items = summarize_items(new_items, language)
    
    if not summarized_items:
        print("No items were successfully summarized. Exiting.")
        return
        
    # Add timestamps and save to daily data file
    today = datetime.now().strftime('%Y-%m-%d')
    for item in summarized_items:
        item['timestamp'] = datetime.now().isoformat()
    
    data_dir = f"data/{language}"
    os.makedirs(data_dir, exist_ok=True)
    daily_file = os.path.join(data_dir, f"{today}.json")
    
    # Load existing daily file if it exists (e.g. running multiple times a day)
    existing_items = []
    if os.path.exists(daily_file):
        with open(daily_file, 'r') as f:
            try:
                existing_items = json.load(f)
            except:
                pass
                
    all_daily_items = existing_items + summarized_items
    with open(daily_file, 'w') as f:
        json.dump(all_daily_items, f, indent=2, ensure_ascii=False)
        
    # Mark as processed in history
    mark_as_processed(summarized_items)
    
    # Generate RSS and Webpage by reading last few days of data (e.g., last 30 items)
    all_history_items = []
    for filename in sorted(os.listdir(data_dir), reverse=True):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename), 'r') as f:
                try:
                    items = json.load(f)
                    all_history_items.extend(items)
                    if len(all_history_items) >= 30:
                        break
                except:
                    pass
                    
    top_items = all_history_items[:30]
    
    print("Generating Webpage...")
    build_webpage(top_items, output_file='index.html', language=language)
    
    print("Generating RSS feed...")
    generate_rss(top_items, output_file='feed.xml', language=language)
    
    print("Daily pipeline complete.")

if __name__ == '__main__':
    main()
