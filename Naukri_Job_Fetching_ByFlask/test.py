import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set the path to the ChromeDriver
chrome_driver_path = r'D:\End To End ML\web_scraping by selenium\Naukri_Job_Fetching\chromedriver_v(118.0.5993.70).exe'
os.environ['PATH'] += os.pathsep + chrome_driver_path

driver = webdriver.Chrome(executable_path=chrome_driver_path)  # Use 'executable_path' to specify the driver path
naukri_url = 'https://www.naukri.com/'
driver.get(naukri_url)
