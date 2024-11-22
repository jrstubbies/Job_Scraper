import requests 
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

# use '.content' instead of '.text' as it holds raw bytes
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")

# find all jobs that have the title including 'python'
python_jobs = results.find_all("h2", string = lambda text: "python" in text.lower())

# look at the great-grandparent of the h2 title tag, this allows the use of other important information
python_job_cards = [ h2_element.parent.parent.parent for h2_element in python_jobs]


# display the job's title, location, and company 
for job in python_job_cards:
    title = job.find("h2", class_="title")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print()

# get the apply link. This site has "learn" and "apply" links. Finding all the <a> tags associated with a job card
# are then indexing to access the SECOND link - which is the 'apply' link (this skips over the 'learn' link)
# then for this link, we want the URL which is found in the 'href' part of the <a>
for job in python_job_cards:
    link_url = job.find_all("a")[1]["href"]
    print(link_url)