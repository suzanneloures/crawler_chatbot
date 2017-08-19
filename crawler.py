import re
from robobrowser import RoboBrowser

vetor_links = []
vetor_titulos = []

# Browse to Rap Genius
browser = RoboBrowser(history=True)
browser.open('http://wiki.dcc.ufba.br/BSI')
links = browser.select('a')
browser.find_all(['h1','h2','h3','h4','h5','h6'])

for link in links:
    if(not link['href'].startswith('http') and link['href'] not in vetor_links):
        vetor_links.append(link['href'])
        browser.open('http://wiki.dcc.ufba.br' + link['href'])
        print(browser.select('title')[0])