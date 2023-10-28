import os
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from urllib.parse import quote  # Use quote from urllib.parse

app = Flask(__name__)

# Set the path to the Chrome driver
chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver_v(118.0.5993.70).exe')
os.environ['PATH'] += os.pathsep + chrome_driver_path

def scrape_naukri(search_query):
    driver = webdriver.Chrome()
    naukri_url = 'https://www.naukri.com/'
    driver.get(naukri_url)

    search_placeholder = driver.find_element(By.CLASS_NAME, "suggestor-input")
    search_query = quote(search_query)  # Encoding user input
    search_placeholder.send_keys(search_query)

    search_button = driver.find_element(By.CLASS_NAME, "qsbSubmit")
    search_button.click()

    # Handle URL transformation
    original_url = "https://www.naukri.com/"
    modified_input = search_query.replace(" ", "-").lower()
    new_url = f"{original_url}{modified_input}-jobs?k={modified_input}"

    # Wait for the URL to change
    timeout = 10
    start_time = time.time()

    job_titles = []
    company_names = []
    experience_required = []
    package_details = []
    locations = []
    skills = []

    for page_number in range(1, 3):
        driver.get(new_url + '&pageNo=' + str(page_number))
        driver.implicitly_wait(10)

        title_elements = driver.find_elements(By.CLASS_NAME, "title")
        for element in title_elements:
            title = element.text
            job_titles.append(title)

        company_elements = driver.find_elements(By.CLASS_NAME, "comp-name")
        for element in company_elements:
            company_name = element.text
            company_names.append(company_name)

        experience_elements = driver.find_elements(By.CLASS_NAME, "expwdth")
        for element in experience_elements:
            experience = element.text
            experience_required.append(experience)

        package_elements = driver.find_elements(By.CLASS_NAME, "ni-job-tuple-icon-srp-rupee")
        for element in package_elements:
            nested_span = element.find_element(By.TAG_NAME, "span")
            package = nested_span.text
            package_details.append(package)

        location_elements = driver.find_elements(By.CLASS_NAME, 'locWdth')
        for element in location_elements:
            location = element.text
            locations.append(location)

        skills_elements = driver.find_elements(By.CLASS_NAME, 'tags-gt')
        for element in skills_elements:
            skill = element.text
            skills.append(skill)

    driver.quit()

    return job_titles, company_names, experience_required, package_details, locations, skills

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    search_query = request.form['search_query']
    job_titles, company_names, experience_required, package_details, locations, skills = scrape_naukri(search_query)

    # Ensure all lists have the same length by padding with "None"
    max_length = max(len(job_titles), len(company_names), len(experience_required), len(package_details), len(locations), len(skills))
    
    job_titles.extend(["None"] * (max_length - len(job_titles)))
    company_names.extend(["None"] * (max_length - len(company_names)))
    experience_required.extend(["None"] * (max_length - len(experience_required)))
    package_details.extend(["None"] * (max_length - len(package_details)))
    locations.extend(["None"] * (max_length - len(locations)))
    skills.extend(["None"] * (max_length - len(skills)))



    data = {
        'Job Titles': job_titles,
        'Company Names': company_names,
        'Experience Required': experience_required,
        'Package Details': package_details,
        'Locations': locations,
        'Skills': skills,
        'search_query': search_query 
    }
    df = pd.DataFrame(data)

    output_file = f'{search_query}_naukri_jobs.csv'
    df.to_csv(output_file, index=False)

    return render_template('results.html', data=df, output_file=output_file,search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
