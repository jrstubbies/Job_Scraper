import requests 
from bs4 import BeautifulSoup
from selenium import webdriver      # as page is dynamic, use selenium to scrape the rendered page
from selenium.webdriver.chrome.options import Options
import time


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


# prevents error about not finding usb drive ?????   -> "--headless=new" stops program working
driver_options = Options()
driver_options.add_argument("--log-level=3")
driver_options.add_argument(f"user-agent={user_agent}")


# setup for webdriver to render 'indeed.com' where the search is for 'software developer' in 'New Zealand'
# use '&start=xx' where xx is the pagination number that want to use
URL = "https://nz.indeed.com/jobs?q=software+developer&l=New+Zealand"
driver = webdriver.Chrome(options = driver_options)
driver.get(URL)

time.sleep(10)   #sleep to allow the results to fully load


# use '.content' instead of '.text' as it holds raw bytes. Close the web driver
soup = BeautifulSoup(driver.page_source, "html.parser")


# results holds the container for all the 'job cards'
results = soup.find(id="mosaic-provider-jobcards")

# find all jobs cards within this container, as giving by a div class of 'job_seen_beacon'
job_cards = results.find_all('div', class_='job_seen_beacon')


# loop through all the job cards (15 per page. pagination does as 'n - 1' where n is the page wanting)
# starting page (page 1) does NOT have a 'start' URL parameter
for job in job_cards:

    # h2 class will have the job name, which is also a link to the full job listing
    job_title = job.find("h2", class_=lambda text: "jobTitle" in text)

    company_container = job.find('a', {'class': 'css-1ioi40n e19afand0'})
    company = company_container.text.strip() if company_container else None

    location_container = job.find('div', {'data-testid': 'inlineHeader-companyLocation'})
    location = location_container.div.text.strip() if location_container else 'Remote or Unknown'

    apply_container = job.find('div', class_ = 'css-199trha eu4oa1w0')
    apply_link = apply_container.find("button")
    apply_url = apply_link["href"]

    description_container = job.find(id="jobDescriptionText")
    description = description_container.text.strip()


    print(job_title.text)
    #print(f"Job URL: {job_title_url}\n")
    print(company)
    print(location)
    print(apply_url)
    print(description)
    print()

driver.quit()
