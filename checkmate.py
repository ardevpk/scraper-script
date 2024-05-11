import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Define the URL you want to scrape
url = "https://example.com"

# Set up the Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--window-size=1920,1080")  # Set window size
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking

# Check if Chromium WebDriver is installed, if not download the latest version
chromedriver_path = "/usr/local/bin/chromedriver"  # Set the path where you want to store Chromedriver

if not os.path.exists(chromedriver_path):
    print("Chromedriver not found. Downloading...")
    os.system("curl -O https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
    latest_release = open("LATEST_RELEASE").read().strip()
    os.system(f"curl -O https://chromedriver.storage.googleapis.com/{latest_release}/chromedriver_linux64.zip")
    os.system("unzip chromedriver_linux64.zip")
    os.system(f"mv chromedriver /usr/local/bin/")
    os.system("rm chromedriver_linux64.zip LATEST_RELEASE")

# Set up the Chrome WebDriver service
service = Service(chromedriver_path)

# Start the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL and wait for a few seconds
driver.get(url)
time.sleep(5)

# Print the page content
print(driver.page_source)

# Close the WebDriver
driver.quit()
