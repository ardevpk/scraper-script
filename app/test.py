import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Initialize Chrome driver with specified binary path

service = Service(os.path.join(os.getcwd(), './scraper/chromedrivers/chromedriver111'))
driver = webdriver.Chrome(options=chrome_options, service=service)

# Example usage: Open Google and get title
driver.get("https://www.google.com")
print("Title:", driver.title)

# Quit the driver
driver.quit()