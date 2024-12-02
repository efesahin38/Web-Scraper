from bs4 import BeautifulSoup  # For parsing HTML and XML documents
import csv  # For reading from and writing to CSV files
from selenium import webdriver
import re  # For regular expression operations
import os  # For interacting with the operating system
from selenium_stealth import stealth

querry=input("company") # Asks the user for a job title or keyword
location=input("Berlin")  # Asks the user for a location
chromeoptions=webdriver.ChromeOptions()
chromeoptions.add_argument("--headless")
chromeoptions.add_argument("start-maximized")
chromeoptions.add_experimental_option("excludeSwitches",["enable-automation"])
chromeoptions.add_experimental_option("useAutomationExtension",False)
base_url = "https://de.indeed.com/jobs?q={query}&l={location1}".format(query=querry, location1=location) # This line formats the base URL with the user-provided query and location.
driver = webdriver.Chrome(options=chromeoptions)  # Initializes the Chrome WebDriver
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
driver.get(base_url)  # Navigates to the specified URL in the web browser
drivers = driver.page_source  # Retrieves the HTML source of the page

soup = BeautifulSoup(drivers, 'html.parser')  # Parses the HTML content using BeautifulSoup
print(soup)

job_postings = soup.find_all('span', id=re.compile("jobTitle"))  # Finds all job postings
job_names = soup.find_all('span', attrs={'data-testid':"company-name"})  # Finds all company names
job_locations = soup.find_all('div', attrs={'data-testid': "text-location"})  # Finds all job locations

jobs = []  # Initializes a list to store job data
for job_posting, job_name, job_location in zip(job_postings, job_names, job_locations):
    jobs.append([job_posting.text, job_name.text, job_location.text])  # Appends job data to the list

driver.quit()  # Closes the web browser

file_path = "C:\\Users\ercan\OneDrive\Masaüstü\Projects\web_scraping\web_scraping\jobs_finder.csv.csv"  # Sets the file path
file_exists = os.path.isfile(file_path)  # Checks if the file already exists

with open(file_path, mode='a', newline='', encoding='utf-8') as file:  # Opens the CSV file
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company Name', 'Location'])  # Writes the header
    for start in range(20, 100, 10):  # Iterates through page numbers
        url = f'{base_url}&start={start}'  # Updates the URL with the new page number
        for job in jobs:  # Iterates through the jobs list
            writer.writerow(job)  # Writes each job to the CSV file

print(f'Job data have been saved to {file_path}')  # Prints a confirmation message