import requests
from bs4 import BeautifulSoup

def fetch_trending_repos():
    url = 'https://github.com/trending'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching GitHub Trending: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    for article in soup.select('article.Box-row'):
        h2 = article.select_one('h2.h3')
        if not h2:
            continue
        a_tag = h2.find('a')
        repo_name = a_tag['href'].strip('/')
        description_p = article.select_one('p.col-9')
        description = description_p.text.strip() if description_p else ''
        repos.append({
            'id': f'github_{repo_name}',
            'title': repo_name,
            'description': description,
            'url': f'https://github.com/{repo_name}',
            'source': 'GitHub Trending'
        })
    return repos

if __name__ == '__main__':
    repos = fetch_trending_repos()
    print(f"Fetched {len(repos)} trending repos.")
    for r in repos[:3]:
        print(r)
