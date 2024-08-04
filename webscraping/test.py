import requests
from bs4 import BeautifulSoup

def scrape_homepage():
    url = 'https://arxiv.org/'
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize a dictionary to hold the categories and their subtopics
    categories = {}

    # Find all the <h2> tags that represent the main categories
    main_categories = soup.find_all('h2')
    subtopics = []
    for category in main_categories: #category str is an h2 section
        # Get the category name 
        category_name = category.text
        
        subtopic_list = category.find_next('ul') #ul division, it's a bunch <li>s
        
        if subtopic_list: 
            subtopic_links = subtopic_list.find_all('a')
            
            for link in subtopic_links:
                link_url = link.get('href')
                if "/list/" in link_url and "/recent" in link_url:
                    # print(link_url, category_name)
                    subtopics.append("https://arxiv.org/" + link_url)
            
            # Add the category and its subtopics to the dictionary
            categories[category_name] = subtopics
        print(subtopics)

    import pickle

    with open('outfile', 'wb') as fp:
        pickle.dump(subtopics, fp)

#https://arxiv.org//list/q-fin.EC/recent
import requests
from bs4 import BeautifulSoup

def scrape_all_papers(base_url='https://arxiv.org/list/cs.AI/recent'):
    papers = []

    def scrape_page(url):
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the papers from the page
        papers_list = soup.find_all('div', class_='meta')
        for paper in papers_list:
            title = paper.find('div', class_='list-title').text.strip()
            authors = paper.find('div', class_='list-authors').text.strip()
            abstract = paper.find('p', class_='abstract').text.strip() if paper.find('p', class_='abstract') else 'No abstract'
            papers.append({'title': title, 'authors': authors, 'abstract': abstract})

        # Find the next page link
        paging_div = soup.find('div', class_='paging')
        next_page_link = None
        if paging_div:
            links = paging_div.find_all('a')
            for link in links:
                if 'Next' in link.text or '>' in link.text:
                    next_page_link = 'https://arxiv.org' + link.get('href')
                    break
        return next_page_link

    next_url = base_url
    while next_url:
        next_url = scrape_page(next_url)

    # Write all papers to a file
    with open("csAItest.txt", "w", encoding='utf-8') as f:
        for paper in papers:
            f.write(f"Title: {paper['title']}\n")
            f.write(f"Authors: {paper['authors']}\n")
            f.write(f"Abstract: {paper['abstract']}\n")
            f.write("\n")

# scrape_all_papers()
  
def save_arxiv_html(url='https://arxiv.org/list/q-bio.NC/recent', file_name='arxiv_crawled_pages/fewer_q-bio.txt'):
    response = requests.get(url)
    html_content = response.text

    # Write the raw HTML content to a file
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Call the function
save_arxiv_html()
 