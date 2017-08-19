import re
from robobrowser import RoboBrowser

# Browse to Rap Genius
browser = RoboBrowser(history=True)
browser.open('http://wiki.dcc.ufba.br/BSI')
browser.select('a')
browser.find_all(['h1','h2','h3','h4','h5','h6'])
