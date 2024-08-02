from get_all_from_subtopic import scrape_articles
import pickle

with open ('outfile', 'rb') as fp:
    itemlist = pickle.load(fp)

for link in itemlist:
    scrape_articles(link)
