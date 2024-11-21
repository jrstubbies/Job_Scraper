import requests 
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

# use '.content' instead of '.text' as it holds raw bytes
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="ResultsContainer")

job_cards = results.find_all("div", class_="card-content")
for job in job_cards:
    title = job.find("h2", class_="title")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    print(title)
    print(company)
    print(location)