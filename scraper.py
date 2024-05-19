from selenium import webdriver
from selenium.webdriver.common.by import By


def setup_webdriver():
    # install_google_chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (optional)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(command_executor='https://standalone-chrome-production-aa0c.up.railway.app', options=options)
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
