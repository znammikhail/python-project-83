from bs4 import BeautifulSoup

def parse_html_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    h1_tag = soup.find('h1')
    if h1_tag:
        h1 = h1_tag.text.strip()
    else:
        h1 = None

    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
    else:
        title = None

    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag and 'content' in meta_tag.attrs:
        description = meta_tag['content'].strip()
    else:
        description = None

    return h1, title, description