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

import urllib.request          # built-in HTTP client 
import urllib.error            # HTTPError / URLError 
import csv                     # optional output
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

#################################
## 2.1 Parse local html_string ##
#################################

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
# <html>
# <head>
# <title>Sample Page</title>
# </head>
# <body>
# .....
# </body>
# </html>

print(soup.title) # <title>Sample Page</title>
print(soup.title.text) # Sample Page (a string type)

print(soup.h1) # <h1>Welcome to Web Scraping</h1>
print(soup.h1.string) # Welcome to Web Scraping (a 'bs4.element.NavigableString' type)

###############################################
## 2.2 Read HTML from a URL (MOST IMPORTANT) ##
###############################################

# Change this URL to your target.
url = "https://quotes.toscrape.com"

# Add headers (many sites behave better with a User-Agent).
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; bs4-learning-script; +https://quotes.toscrape.com)"
}

# urllib.request supports Request objects + headers + timeout. 
req = urllib.request.Request(url, headers=headers)

html_bytes = None
final_url = None

try:
    with urllib.request.urlopen(req, timeout=15) as resp:  # timeout avoids hanging 
        final_url = resp.geturl()
        html_bytes = resp.read()
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code, e.reason)
except urllib.error.URLError as e:
    print("URLError:", e.reason)
except TimeoutError:
    print("TimeoutError")

# If download succeeded, replace the soup with live page content and use it for EVERYTHING below.
if html_bytes is not None:
    # BS4 can accept bytes; if you pass bytes, it assumes UTF-8 by default. 
    # For many pages this is fine; if you hit encoding issues, decode yourself using the server charset.
    soup = BeautifulSoup(html_bytes, "html.parser")  # live soup source 
    print("Downloaded from:", final_url)
    print("From URL -> soup.title =", soup.title)
else:
    print("Falling back to html_string soup (URL fetch failed).")
    
'''
OUTPUT:

Downloaded from: https://quotes.toscrape.com
From URL -> soup.title = <title>Quotes to Scrape</title>
'''

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

# Find the first <a> tag
print(soup.find("a"))  
# <a href="/" style="text-decoration: none">Quotes to Scrape</a>
# may be None if page has no links 

first_a = soup.find("a")

print(first_a.name)  # a
print(first_a.attrs) # {'href': '/', 'style': 'text-decoration: none'}
print(first_a['href'])  # /
print(first_a.get('style'))  # text-decoration: none


#------------------------------------------------------------------------------------------------#
#------------------------------ 4. Navigate the parse tree --------------------------------------#
#------------------------------------------------------------------------------------------------#

body = soup.body  # may be None if HTML is fragment or unusual
print("Has <body>:", body is not None)

if body:
    # children includes text nodes like '\n'
    body_children = list(body.children)
    print("len(list(body.children)):", len(body_children))

    # example: get the first element child (skip text nodes)
    first_element_child = None
    for node in body_children:
        if getattr(node, "name", None) is not None:  # Tag nodes have .name
            first_element_child = node
            break

    print("First element child under <body>:", first_element_child)

    if first_element_child:
        next_sib = first_element_child.find_next_sibling()  # skips text nodes 
        print("Next sibling element:", next_sib)
else:
    print("No <body> tag available; navigation examples will be limited.")


#------------------------------------------------------------------------------------------------#
#------------------------------ 5. Searching (find / find_all) safely ---------------------------#
#------------------------------------------------------------------------------------------------#

'''
- find(...) -> first match or None 
- find_all(...) -> list (possibly empty) 
'''

all_links = soup.find_all("a")  # list 
print("Number of <a> tags:", len(all_links))

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

# Safe None-handling pattern
maybe_title = soup.find("title")  # Tag or None 
title_text = maybe_title.get_text(strip=True) if maybe_title else None
print("Safe title_text:", title_text)


#------------------------------------------------------------------------------------------------#
#------------------------------ 6. Text extraction ----------------------------------------------#
#------------------------------------------------------------------------------------------------#

'''
- .string is only reliable when a tag has a single direct text node. 
- .get_text(strip=True) is robust for “all text under this tag”. 
'''

h1 = soup.find("h1")
if h1:
    print("h1.string:", h1.string)  # may be None if nested tags exist
    print("h1.get_text(strip=True):", h1.get_text(strip=True))  # robust 
else:
    print("No <h1> found.")


#------------------------------------------------------------------------------------------------#
#------------------------------ 7. CSS selectors (select / select_one) --------------------------#
#------------------------------------------------------------------------------------------------#

'''
CSS selectors:
- select("CSS") -> list
- select_one("CSS") -> first match or None
Docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 
'''

all_paragraphs = soup.select("p")
print("Number of <p> tags (via select):", len(all_paragraphs))

first_p = soup.select_one("p")
if first_p:
    print("First <p> text:", first_p.get_text(" ", strip=True))
else:
    print("No <p> found.")


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
if rows[:3]:
    print("First rows sample:", rows[:3])

# Optional: write to CSV
# output_path = "links.csv"
# with open(output_path, "w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=["text", "href"])
#     writer.writeheader()
#     writer.writerows(rows)


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
