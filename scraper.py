import requests 
from bs4 import BeautifulSoup
from selenium import webdriver      # as page is dynamic, use selenium to scrape the rendered page
from selenium.webdriver.chrome.options import Options
import time

# prevents error about not finding usb drive ?????   -> "--headless=new" stops program working
driver_options = Options()
driver_options.add_argument("--log-level=3")


# setup for webdriver to render 'indeed.com' where the search is for 'software developer' in 'New Zealand'
# use '&start=xx' where xx is the pagination number that want to use
URL = "https://nz.indeed.com/jobs?q=software+developer&l=New+Zealand"
driver = webdriver.Chrome(options = driver_options)
driver.get(URL)

time.sleep(1)   #sleep to allow the results to fully load


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
    job_link = job_title.find("a")           

    # need to add the domain to this url                                              
    job_title_url = "https://nz.indeed.com" + job_link["href"]

    # use driver to scrape each of these job pages
    driver.get(job_title_url)
    soup2 = BeautifulSoup(driver.page_source, "html.parser")

    # now scraping the information for each of the job pages
    job_company = soup2.find('a', {'class': 'css-1ioi40n e19afand0'})
    company_text = job_company.text.strip() if job_company else None        # doesnt work at this point

    job_location = soup2.find('div', {'data-testid': 'inlineHeader-companyLocation'})
    location_text = job_location.div.text.strip() if job_location else None

    print(job_title.text)
    #print(f"Job URL: {job_title_url}\n")
    print(company_text)
    print(location_text)
    print()

driver.quit()
