from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Initialize Chrome driver with specified binary path
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, executable_path='./scraper/chromedrivers/chromedriver')

# Example usage: Open Google and get title
driver.get("https://www.google.com")
print("Title:", driver.title)

# Quit the driver
driver.quit()