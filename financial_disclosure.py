import requests
from bs4 import BeautifulSoup
import os

url = 'https://disclosures-clerk.house.gov'
data = {"LastName": "pelosi"}
response = requests.post(f'{url}/FinancialDisclosure/ViewMemberSearchResult', data=data)

createdDocumentUrls = {}
if 'documentUrls.txt' in os.listdir():
    with open('documentUrls.txt', 'r') as f:
        createdDocumentUrls = eval(f.read())

parsed_html = BeautifulSoup(response.text, 'html.parser')
fillings = parsed_html.find_all('tr', attrs={'role':'row'})
fillings.pop(0)

# sort fillings by year
fillings.sort(key=lambda x: int(x.find_all('td', attrs={"data-label": "Filing Year"})[0].text))
documentUrls = {}
for filling in fillings:
    key = filling.find_all('td', attrs={"data-label": "Filing Year"})[0].text
    url = f'{url}/{filling.a.get("href")}'
    arr = documentUrls.get(key, [])
    documentUrls[key] = arr + [url]


print(len(documentUrls))
# save the documentUrls to a file
with open('documentUrls.txt', 'w') as f:
    f.write(str(documentUrls))
