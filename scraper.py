import requests 
from bs4 import BeautifulSoup
from selenium import webdriver      # as page is dynamic, use selenium to scrape the rendered page


# setup for webdriver to render 'indeed.com' where the search is for 'software developer' in 'New Zealand'
# use '&start=xx' where xx is the pagination number that want to use
URL = "https://nz.indeed.com/jobs?q=software+developer&l=New+Zealand"
driver = webdriver.Chrome()
driver.get(URL)

# use '.content' instead of '.text' as it holds raw bytes
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()


# results holds the container for all the 'job cards'
results = soup.find(id="mosaic-provider-jobcards")

# find all jobs that have the title including 'python'
job_cards = results.find_all('div', class_='job_seen_beacon')

# loop through all the job cards (15 per page. pagination does as 'n - 1' where n is the page wanting)
# e.g. page 2 would be https....&start=1
# page 8 would be https....start=7
for job in job_cards:
    job_title = job.find("h2", class_=lambda text: "jobTitle" in text)
    job_link = job_title.find("a")                                                          # IS NOT GETTING THE CORRECT LINK !!!!
    job_title_url = job_link["href"]
    print(job_title.text)
    print(f"Job URL: {job_title_url}\n")
    print()
