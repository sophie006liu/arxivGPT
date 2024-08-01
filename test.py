import requests
from bs4 import BeautifulSoup

# Fetch the arXiv main page
url = 'https://arxiv.org/'
response = requests.get(url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a dictionary to hold the categories and their subtopics
categories = {}

# Find all the <h2> tags that represent the main categories
main_categories = soup.find_all('h2')

for category in main_categories:
    # Get the category name
    category_name = category.text
    
    # Find the next <ul> tag which contains the subtopics for this category
    subtopic_list = category.find_next('ul')
    
    if subtopic_list:
        # Initialize a list to hold the subtopics
        subtopics = []
        
        # Find all the <a> tags within the <ul> tag
        subtopic_links = subtopic_list.find_all('a')
        
        for link in subtopic_links:
            subtopics.append(link.text)
        
        # Add the category and its subtopics to the dictionary
        categories[category_name] = subtopics

# Print the categories and their subtopics
for category, subtopics in categories.items():
    print(f"{category}:")
    for subtopic in subtopics:
        print(f"  - {subtopic}")

