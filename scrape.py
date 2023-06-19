from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from helpers import convertSalaryRange
import logging

logging.basicConfig(filename='errors.log', level=logging.DEBUG)
def indeedScrape(jobTitle, location, pages):
    '''
    Creates a list of dictionaries containing job details from Indeed.
    Utilizes headless Chrome browser to scrape data.
    '''
    options = Options()
    options.headless = False
    user_agent =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    # Set up Selenium webdriver
    driver = webdriver.Chrome(options=options)
    #  convert jobTitle and location to url format
    jobTitle = jobTitle.replace(" ", "+")
    location = location.replace(" ", "+")
    cleaned_job_postings = []
    # List to store errors for further degbugging.
    page_errors = []
    for page in range(pages):
        try:
            # Specify the URL of the job search results page on Indeed
            page = page * 10
            url = f'https://sg.indeed.com/jobs?q={jobTitle}&l={location}&start={page}&from=searchOnHP&vjk=905433ec4a09c937'

            # Open the URL in the browser
            driver.get(url)
            
            time.sleep(5)
            # Find the job postings on the page
            job_postings = driver.find_elements(By.XPATH, '//div[@class="slider_container css-8xisqv eu4oa1w0"]')
            # Extract data from each job posting
            for posting in job_postings:
                title_ele =  posting.find_element(By.TAG_NAME, 'span')
                company_ele = posting.find_element(By.XPATH, './/span[@class="companyName"]')
                jobLink = posting.find_element(By.XPATH, './/a[@class="jcs-JobTitle css-jspxzf eu4oa1w0"]')
                salary_package = [None, None]
                try:
                    # Get salary if available
                    salary_ele = posting.find_element(By.XPATH, './/div[@class="metadata salary-snippet-container"]')
                    salary = salary_ele.text.strip()
                    salary_package = convertSalaryRange(salary)
                except Exception as e:
                    pass

                title = title_ele.text.strip()
                company = company_ele.text.strip()
                jobLink = jobLink.get_attribute('href')

                cleaned_job_postings.append({
                    "JobTitle": title,
                    "CompanyName": company,
                    "SalaryLower": salary_package[0],
                    "SalaryUpper": salary_package[1],
                    "JobLink": jobLink
                })

            
            driver.quit()
            # Prevent getting blocked by Indeed
            time.sleep(4)
        except Exception as e:
            logging.error(str(e))
            page_errors.append(str(e))

    return cleaned_job_postings, page_errors


if __name__ == "__main__":
    jobTitle = "Software Engineer"
    location = "Singapore"
    job_details = indeedScrape(jobTitle, location, 2)
    print(job_details)