'''
BeautifulSoup4 (bs4) parses HTML/XML into a navigable tree so you can search, navigate, and extract data. 

This script is organized in a learn-first order:
- Parse a local HTML string (for sanity checks),
- Immediately fetch HTML from a URL and replace the soup with live content,
- Use that live soup for navigation/search/extraction patterns. 

Docs:
- Beautiful Soup official docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
- urllib.request (built-in): https://docs.python.org/3/library/urllib.request.html 

###################################

Flow of contents:

1. HTML structure basics
2. Parse html_string, then read HTML from URL
3. Inspect tags/text/attributes
4. Navigate the parse tree (parent/children/siblings)
5. Search (find / find_all) with safe None-handling
6. Text extraction (text vs string vs get_text)
7. CSS selectors (select / select_one)
8. Extraction loop pattern (optional CSV write)
9. Common scraping gotchas (missing tags, encoding, timeouts)

No def/class used, only built-in modules + bs4. 
'''

from bs4 import BeautifulSoup  # bs4 docs: BeautifulSoup(markup, 'html.parser') 
import requests                # Read HTLM documents from URLs
import time                    # optional pacing


#------------------------------------------------------------------------------------------------#
#----------------------------------- 1. HTML structure basics -----------------------------------#
#------------------------------------------------------------------------------------------------#

'''
Minimal expected HTML skeleton:

<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <h1>Heading</h1>
    <p>Paragraph with a <a href="...">link</a>.</p>
    <ul><li>Item</li></ul>
  </body>
</html>
'''


#------------------------------------------------------------------------------------------------#
#-------------------------- 2. Parse html_string, then read from URL ----------------------------#
#------------------------------------------------------------------------------------------------#

#############################
## Parse local html_string ##
#############################

html_string = """
<html>
  <head>
    <title>Sample Page</title>
  </head>
  <body>
    <h1>Welcome to Web Scraping</h1>
    <p>Python is great for data science.</p>
    <p>Machine learning requires quality data.</p>
    <h2>Data Sources</h2>
    <ul>
      <li>Wikipedia</li>
      <li>GitHub</li>
      <li>arXiv</li>
    </ul>
    <a href="https://example.com/about" class="nav">About</a>
  </body>
</html>
"""

# Initial parse from local string (for sanity checks) 
soup = BeautifulSoup(html_string, "html.parser")

# Verify initial parse
print(soup)
'''
<html>
<head>
<title>Sample Page</title>
</head>
<body>
.....
</body>
</html>
'''

#############

print(soup.title) # <title>Sample Page</title>
print(soup.title.text) # Sample Page (a string type)

print(soup.h1) # <h1>Welcome to Web Scraping</h1>
print(soup.h1.string) # Welcome to Web Scraping (a 'bs4.element.NavigableString' type)

###########################################
## Read HTML from a URL (MOST IMPORTANT) ##
###########################################

# Change this URL to your target.
url = "https://quotes.toscrape.com"

# Get HTLM document
req = requests.get(url)
html_content = req.text  # string (Unicode)

# Parse HTML from URL
soup = BeautifulSoup(html_content, "html.parser")

print(soup.title)
'''<title>Quotes to Scrape</title>'''

print(soup)
'''
<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Quotes to Scrape</title>
<link href="/static/bootstrap.min.css" rel="stylesheet"/>
<link href="/static/main.css" rel="stylesheet"/>
</head>
<body>
<div class="container">
<div class="row header-box">
<div class="col-md-8">
<h1>
<a href="/" style="text-decoration: none">Quotes to Scrape</a>
...
(more contents)
'''


#------------------------------------------------------------------------------------------------#
#------------------------------ 3. Inspect tags / text / attributes -----------------------------#
#------------------------------------------------------------------------------------------------#

'''
Core objects:
- BeautifulSoup: whole document
- Tag: element nodes like <a>, <div>, <p>
- Text nodes: strings inside tags
Docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
'''

print(soup.name) # Usually '[document]' for the root
# [document]

# Find the first <a> tag (link)
print(soup.find("a"))  
'''
<a href="/" style="text-decoration: none">Quotes to Scrape</a>
may be None if page has no links 
'''

first_a = soup.find("a")

print(first_a.name)  # a
print(first_a.attrs) # {'href': '/', 'style': 'text-decoration: none'}
print(first_a['href'])  # /
print(first_a.get('style'))  # text-decoration: none
print(first_a.get_text(strip=True))  # Quotes to Scrape


#------------------------------------------------------------------------------------------------#
#------------------------------ 4. Navigate the parse tree --------------------------------------#
#------------------------------------------------------------------------------------------------#

body = soup.body  # may be None if HTML is fragment or unusual
print("Has <body>:", body is not None)
# Has <body>: True

print(body.children) # <generator object Tag.children.<locals>.<genexpr> at 0x7b905973b400>

body_children = list(body.children)
print(body_children)
'''
['\n', <div class="container">
<div class="row header-box">
<div class="col-md-8">
..., '\n']
'''

print(body_children.count('\n')) # '\n' are text
# 3

######################

first_element_child = None
for node in body_children: # get the first element child (skip text nodes)
    if getattr(node, "name", None) is not None:  # Check if that node has a 'name' attribute (i.e., is a Tag)
        first_element_child = node # Assign that node to first_element_child if it has a 'name' attribute
        break

print(f"First element child under <body>:\n{first_element_child}")
'''
<div class="container">
<div class="row header-box">
<div class="col-md-8">
...
(more contents)
'''

######################

# Find next sibling of that first element child (skipping text nodes)
next_sibling = first_element_child.find_next_sibling()

print(f"Next sibling of first element child:\n{next_sibling}")
'''
<footer class="footer">
<div class="container">
<p class="text-muted">
                Quotes by: <a href="https://www.goodreads.com/quotes">GoodReads.com</a>
</p>
<p class="copyright">
                Made with <span class="zyte">❤</span> by <a class="zyte" href="https://www.zyte.com">Zyte</a>
</p>
</div>
</footer>
'''


#------------------------------------------------------------------------------------------------#
#------------------------------ 5. Searching (find / find_all) safely ---------------------------#
#------------------------------------------------------------------------------------------------#

'''
- find(...) -> first match or None 
- find_all(...) -> list (possibly empty)
'''

#############
## .find() ##
#############

first_quote = soup.find(name="span", class_="text")  # Tag or None

print(first_quote)
'''
<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. 
It cannot be changed without changing our thinking.”</span>
'''

print(first_quote.attrs) # {'class': ['text'], 'itemprop': 'text'}
print(first_quote['class'])  # ['text']
print(first_quote.get('itemprop'))  # text

print(first_quote.get_text(strip=True)) # strip=True removes surrounding whitespace
'''
“The world as we have created it is a process of our thinking. 
It cannot be changed without changing our thinking.”
'''

#################
## .find_all() ##
#################

all_links = soup.find_all("a")  # list

print(all_links[:3])  # print first few <a> tags
'''
[<a href="/" style="text-decoration: none">Quotes to Scrape</a>, 
<a href="/login">Login</a>, 
<a href="/author/Albert-Einstein">(about)</a>]
'''

print("Number of <a> tags:", len(all_links))
# Number of <a> tags: 55

######################

# Print first few links (safe)
max_show = 5
count = 0
for a in all_links:
    if count >= max_show:
        break
    text = a.get_text(strip=True)
    href = a.get("href")
    print("Link:", text, "=>", href)
    count += 1
'''
Link: Quotes to Scrape => /
Link: Login => /login
Link: (about) => /author/Albert-Einstein
Link: change => /tag/change/page/1/
Link: deep-thoughts => /tag/deep-thoughts/page/1/
'''

######################

# Safe None-handling pattern
maybe_title = soup.find("title")  # Tag or None 
title_text = maybe_title.get_text(strip=True) if maybe_title else None # Get the text safely (if it is not None)

print("Safe title_text:", title_text)
# Safe title_text: Quotes to Scrape


#------------------------------------------------------------------------------------------------#
#----------------------------------- 6. Text extraction -----------------------------------------#
#------------------------------------------------------------------------------------------------#

'''
- .string is only reliable when a tag has a single direct text node. 
- .get_text(strip=True) is robust for “all text under this tag”. 
'''

h1 = soup.find("h1")

print(h1)
'''
<h1>
<a href="/" style="text-decoration: none">Quotes to Scrape</a>
</h1>
'''

#########################################

print(h1.string)
# None
'''Returns None because <h1> has a child <a> tag, so it is not a single text node.'''

print(h1.get_text(strip=True))
# Quotes to Scrape

###########################
## Demo single text node ##
###########################

first_a = soup.find("a")

print(first_a)
# <a href="/" style="text-decoration: none">Quotes to Scrape</a>

print(first_a.string)
# Quotes to Scrape
'''Because <a> has only one direct text node, .string works here.'''


#------------------------------------------------------------------------------------------------#
#------------------------------ 7. CSS selectors (select / select_one) --------------------------#
#------------------------------------------------------------------------------------------------#

'''
CSS selectors:
- select("CSS") -> list
- select_one("CSS") -> first match or None
Docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
'''

###############
## .select() ##
###############

all_paragraphs = soup.select("p")

print(all_paragraphs)
'''
[<p>
<a href="/login">Login</a>
</p>, <p class="text-muted">
                Quotes by: <a href="https://www.goodreads.com/quotes">GoodReads.com</a>
</p>, <p class="copyright">
                Made with <span class="zyte">❤</span> by <a class="zyte" href="https://www.zyte.com">Zyte</a>
</p>]
'''

print(len(all_paragraphs))
# 3

###################
## .select_one() ##
###################

first_p = soup.select_one("p")

print(first_p)
'''
<p>
<a href="/login">Login</a>
</p>
'''

print(first_p.get_text(strip=True))
# Login


#------------------------------------------------------------------------------------------------#
#------------------------------ 8. Extraction loop pattern (+ CSV optional) ---------------------#
#------------------------------------------------------------------------------------------------#

rows = []
for a in soup.find_all("a"):  # list of Tag 
    rows.append({
        "text": a.get_text(" ", strip=True),
        "href": a.get("href")
    })

print("Extracted link rows:", len(rows))
# Extracted link rows: 55

for idx, row in enumerate(rows[:5]):  # print first few rows
    print(f"Row {idx+1}: Text='{row['text']}', Href='{row['href']}'")
'''
Row 1: Text='Quotes to Scrape', Href='/'
Row 2: Text='Login', Href='/login'
Row 3: Text='(about)', Href='/author/Albert-Einstein'
Row 4: Text='change', Href='/tag/change/page/1/'
Row 5: Text='deep-thoughts', Href='/tag/deep-thoughts/page/1/'
'''

#############################
## Write to CSV (optional) ##
#############################

'''
import csv

output_path = "links.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "href"])
    writer.writeheader()
    writer.writerows(rows)
'''


#------------------------------------------------------------------------------------------------#
#------------------------------ 9. Common gotchas (practical) -----------------------------------#
#------------------------------------------------------------------------------------------------#

'''
1) Missing elements are normal:
   - Any find/select might return None (single) or [] (list). Guard before using .text/.get_text(). 

2) Encoding:
   - BS4 converts documents to Unicode internally; passing bytes assumes UTF-8 unless you decode yourself. 

3) Networking:
   - Always set a timeout for urlopen to avoid indefinite hanging. 

4) Rate limiting:
   - Use sleep between requests when scraping multiple pages.
'''

time.sleep(0.25)
