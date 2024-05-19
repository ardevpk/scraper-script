import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def install_google_chrome():
    # Check if Google Chrome is installed
    if subprocess.call(['which', 'google-chrome']) == 0:
        print("Google Chrome is already installed.")
        return

    # Download Google Chrome
    subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)

    # Install Google Chrome
    subprocess.run(['sudo', 'apt', 'install', './google-chrome-stable_current_amd64.deb', '-y'], check=True)

    # Fix any broken dependencies
    subprocess.run(['sudo', 'apt', '--fix-broken', 'install', '-y'], check=True)

    print("Google Chrome installation completed.")

def setup_webdriver():
    install_google_chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (optional)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/google-chrome'  # Path to the Chrome binary
    
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_dummy_data():
    driver = setup_webdriver()
    try:
        driver.get('https://httpbin.org/ip')  # Dummy website to scrape data
        response_element = driver.find_element(By.TAG_NAME, 'body')
        print(response_element.text)
        return response_element.text
    finally:
        driver.quit()

# if __name__ == '__main__':
#     install_google_chrome()
#     scrape_dummy_data()
