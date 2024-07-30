import requests
from bs4 import BeautifulSoup

# Function to fetch and parse the subreddit page
def fetch_subreddit(subreddit, num_posts=10):
    url = f'https://www.reddit.com/r/{subreddit}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f'Failed to load page {url}')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    posts = []
    count = 0
    
    for post in soup.find_all('div', class_='_1oQyIsiPHYt6nx7VOmd1sz'):
        if count >= num_posts:
            break
        
        title = post.find('h3')
        if title:
            title_text = title.get_text()
            link = post.find('a', class_='SQnoC3ObvgnGjWt90zD9Z')['href']
            if not link.startswith('http'):
                link = 'https://www.reddit.com' + link
            posts.append({'title': title_text, 'link': link})
            count += 1
    
    return posts

# Example usage
subreddit_name = 'learnpython'
num_posts = 10
posts = fetch_subreddit(subreddit_name, num_posts)

for idx, post in enumerate(posts):
    print(f"Post {idx + 1}:")
    print(f"Title: {post['title']}")
    print(f"Link: {post['link']}")
    print('-' * 30)
