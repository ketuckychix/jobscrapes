import mysql.connector
from db import DB
from scrape import indeedScrape

if __name__ == "__main__":
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="22dec2018",
    database="indeed")
    
    # Scrape data from Indeed.
    jobTitle = "Software Engineer"
    location = "Singapore"
    job_details = indeedScrape(jobTitle, location, 2)
    
    # Create a database object
    db_instance = DB(db)
    print(job_details)
    # Add scraped data to database
    for detail in job_details:
        db_instance.insert(
            "jobs", "JobTitle, CompanyName, SalaryLower, SalaryUpper, JobLink", 
            f"'{detail['JobTitle']}', '{detail['CompanyName']}', {detail['SalaryLower']}, {detail['SalaryUpper']}, '{detail['JobLink']}'")
        db.commit()