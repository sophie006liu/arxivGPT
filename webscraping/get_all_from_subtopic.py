import requests
import re, os
from bs4 import BeautifulSoup

"""
Takes website url and returns the website HTML
"""
def fetch_html(url):
    response = requests.get(url)
    return response.text

"""
Takes HTML, finds list-title class object and returns article names
"""
def extract_article_names(soup):
    articles = []
    for div in soup.find_all('div', class_='meta'):
        title_div = div.find('div', class_='list-title')
        if title_div:
            title = title_div.text.strip().replace('Title:', '').strip()
            articles.append(title)
    return articles

def extract_category(url):
    # Use regex to find the pattern that matches the category part of the URL
    match = re.search(r'/list/([^/]+)/recent', url)
    if match:
        return match.group(1)
    else:
        return None
    
def scrape_articles(base_url='https://arxiv.org/list/cs.IR/recent'):
    html_content = fetch_html(base_url)
    soup = BeautifulSoup(html_content, 'html.parser')

    morefewer_div = soup.find('div', class_='morefewer')
    all_link = None

    if morefewer_div:
        for link in morefewer_div.find_all('a'):
            if 'all' in link.text:
                all_link = 'https://arxiv.org' + link.get('href')
                break

    if all_link:
        print(f"Fetching all articles from: {all_link}")
        html_content = fetch_html(all_link)
        soup = BeautifulSoup(html_content, 'html.parser')

    articles = extract_article_names(soup)
    
    name = base_url[24:-8] 

    with open(f"0_{name}.txt", "w", encoding='utf-8') as f:
        for article in articles:
            f.write(f"{article}\n")

    print(f"Total articles fetched: {len(articles)}")

# Call the function
# scrape_articles()