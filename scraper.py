import requests 
from bs4 import BeautifulSoup
from selenium import webdriver      # as page is dynamic, use selenium to scrape the rendered page


# setup for webdriver to render 'indeed.com' where the search is for 'software developer' in 'New Zealand'
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

for job in job_cards:
    print(job.text)
