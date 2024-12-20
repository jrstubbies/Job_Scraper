import requests 
from bs4 import BeautifulSoup
from selenium import webdriver      # as page is dynamic, use selenium to scrape the rendered page
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# some headers to help avoid authentication issues
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

#sleep to allow the results to fully load
time.sleep(3)   

# use '.content' instead of '.text' as it holds raw bytes. Close the web driver
soup = BeautifulSoup(driver.page_source, "html.parser")

# results holds the container for all the 'job cards'
results = soup.find(id="mosaic-provider-jobcards")

# find all jobs cards within this container
job_cards = results.find_all('div', class_='job_seen_beacon')


# loop through all the job cards (15 per page. pagination does as 'n - 1' where n is the page wanting)
# starting page (page 1) does NOT have a 'start' URL parameter
for job in job_cards:

    # h2 class will have the job name
    job_title = job.find("h2", class_=lambda text: "jobTitle" in text)
    if job_title is None:
        print('job title is none')

    # get the company name
    company_container = job.find('a', {'class': 'css-1ioi40n e19afand0'})
    company = company_container.text.strip() if company_container else None

    # get the jobs location 
    location_container = job.find('div', {'data-testid': 'inlineHeader-companyLocation'})
    location = location_container.div.text.strip() if location_container else 'Remote or Unknown'


    # find the h2 element, want Selenium to click this element so that right pane opens up tp search for details.
    job_link_tag = job_title.find("a")
    if job_link_tag is None:
        print("job link tag is none")
        break

    job_href = job_link_tag.get("href")
    if job_href is None:
        print("the job link tag exists, but the href value is None")
        break

    try:
        selenium_link = driver.find_element(By.XPATH, f"a//[@href='https://nz.indeed.com/{job_href}']")
        selenium_link.click()
    except Exception as e:
        print(f"error finding or clicking the job link: {e}")


    # the container for the right side pop-up containing detailed version of the job. Needs to click job to open
    right_pane_container = soup.find('div', id='jobsearch-ViewjobPaneWrapper')
    if right_pane_container is None:
        print("right pane is none")
    else:
        print("right pane has something")
#-----------------------------------------------------------------------------------------------------------------------------
    # GET THE APPLY BUTTON LINK ??
    apply_container = right_pane_container.find('div', id='applyButtonLinkContainer')
    if apply_container:
        apply_button = apply_container.find('button')
        if apply_button:
            apply_link = apply_button.get('href')
        else:
            apply_button = "no apply button found"
            apply_link = "no link found"
    else:
        apply_container = "no apply container found"
        apply_link = "not found the apply link container"


    # GET THE JOB DESCRIPTION ???
    description_container = right_pane_container.find('div', id='jobDescriptionText')
    if description_container:
        description_text = description_container.get_text(strip=True, separator = "\n")
    else:
        description_container = "no desc container found"
        description_text = "not found description"

    # print all this information to the console. Change this to print to a file????
    print(f"Job title: {job_title.text}")
    print(f"Comany Name: {company}")
    print(f"Comany Location: {location}")
    print(f"Apply Here: {apply_link}")
    print(f"Job Description: '\n' {description_text}")
    print()

    # helps prevent sending multiple requests in quick succession, helps avoid authentication issues ??
    time.sleep(random.uniform(3, 7))

driver.quit()
