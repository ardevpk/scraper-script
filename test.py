from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome options
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--lang=en-US")
options.add_argument("--window-size=1920,1080")
options.add_argument('--start-maximized')
options.add_argument("--proxy-server='direct://'")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--proxy-bypass-list=*")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)


def check_cloudflare_and_solve(driver):
    try:
        # Wait for Cloudflare challenge to be visible
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "cf-challenge-running"))
        # )
        # Wait for the checkbox to be visible
        checkbox = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="checkbox"]'))
        )
        print("Cloudflare checkbox detected, clicking on it...")
        checkbox.click()
        print("Cloudflare challenge detected, waiting for it to complete...")
        time.sleep(15)  # Adjust sleep time as necessary for the challenge to complete
        return True
    except Exception as exc:
        print("No Cloudflare challenge detected.", exc)
        return False

def wait_for_class(driver, class_name, timeout=30):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return element
    except Exception as e:
        print(f"Error waiting for class {class_name}: {e}")
        return None

def process_url(url, desired_class):
    print(f"Processing URL: {url}")
    driver.get(url)

    # Check for the desired class
    element = wait_for_class(driver, desired_class)

    # If the class is not present, check for Cloudflare challenge
    if not element:
        cloudflare_solved = check_cloudflare_and_solve(driver)
        if cloudflare_solved:
            # After waiting for Cloudflare challenge, wait for redirection to complete
            WebDriverWait(driver, 30).until(
                lambda d: d.current_url != url
            )
            final_url = driver.current_url
            print(f"Redirected to: {final_url}")
            element = wait_for_class(driver, desired_class, timeout=30)

    # Check again for the desired class after potential Cloudflare challenge and redirection
    if element:
        print("Desired element found:", element.text)
        return driver.page_source
    else:
        driver.save_screenshot('./test.png')
        print("Desired element not found, and no Cloudflare challenge present or challenge not solved.")
        return None

# Define the URLs and class to check
urls = [
    "https://www.ziprecruiter.com/candidate/search?radius=5000&days=5&search=Python&location=Texas",  # Replace with your target URLs
    "https://www.ziprecruiter.com/candidate/search?radius=5000&days=5&search=Python&location=Florida",
    # Add more URLs as needed
]
desired_class = "job_result_wrapper"  # Replace with the desired class name

for url in urls:
    try:
        page_source = process_url(url, desired_class)
        if page_source:
            print('Found page source!')
            # Use BeautifulSoup to parse the page source if needed
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            # Continue processing with BeautifulSoup as needed
        time.sleep(2)  # Optional: sleep between requests to avoid rate limiting
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Close the driver
driver.quit()
