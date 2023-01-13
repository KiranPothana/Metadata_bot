import requests
from bs4 import BeautifulSoup

url = 'https://arxiv.org/abs/2212.11021'
url = url + "?show=bib"

session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

csrftoken = soup.find('input', {'name': 'csrf_token'})
if csrftoken:
    csrftoken = csrftoken['value']
    session.headers.update({'referer': url})

    payload = {
        'csrf_token': csrftoken,
        'show': 'bib'
    }

    response = session.post(url, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print("Could not find csrf_token, the scraping might not work.")

# Extract the authors
authors = [a.text for a in soup.find_all('div', class_='authors')]

# Extract the abstract
abstract = soup.find('blockquote', class_='abstract mathjax')

# Extract the citations
references = []
references_containers = soup.find_all('p', class_='btn btn-secondary btn-sm')
if references_containers:
    for reference in references_containers:
        references.append(reference.text)
else:
    print("No references found.")

# Print the results
print('Authors:', authors)
print('#############################')
print('Abstract:', abstract.text)
print('#############################')
print('References:', references)
