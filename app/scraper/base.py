from abc import abstractmethod
import os
import ast

from app.scraper.constants import headers

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
from playwright.sync_api import sync_playwright
# from playwright_stealth import stealth_sync


class Script:

    def __init__(self) -> None:
        self.keywords = ["Python", "Django", "FastAPI"]
        self.locations = []

    def get_headers(self):
        print('Headers called!')
        return headers
    
    def get_driver(self):
        print('Options called!')
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-extensions",
                        "--disable-gpu",
                        "--disable-notifications",
                        "--disable-popup-blocking",
                        "--disable-infobars",
                        "--no-sandbox",
                        "--lang=en-US",
                        "--window-size=1920,1080",
                        "--start-maximized",
                        "--proxy-server='direct://'",
                        "--disable-dev-shm-usage",
                        "--proxy-bypass-list=*",
                    ],
                )
                context = browser.new_context(
                    accept_downloads=True,
                    # user_agent=headers,
                    viewport={"width": 1920, "height": 1080},
                    java_script_enabled=True
                )

                # Set other headers
                for header, value in headers.items():
                    context.set_extra_http_headers({header: value})
                page = context.new_page()
                self.run(runner=None, page=page)
                # return page
        except Exception as e:
            print('Error:', e)
            return None

    # def get_options(self):
    #     print('Options called!')
    #     try:

    #         options = Options()
    #         options.add_argument("--disable-blink-features=AutomationControlled")
    #         options.add_argument("--disable-extensions")
    #         options.add_argument("--disable-gpu")
    #         options.add_argument("--disable-notifications")
    #         options.add_argument("--disable-popup-blocking")
    #         options.add_argument("--disable-infobars")
    #         options.add_argument("--no-sandbox")
    #         options.add_argument("--headless")
    #         options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #         options.add_experimental_option('useAutomationExtension', False)
    #         options.add_argument("--lang=en-US")
    #         options.add_argument("--window-size=1920,1080")
    #         options.add_argument('--start-maximized')
    #         options.add_argument("--proxy-server='direct://'")
    #         options.add_argument('--disable-dev-shm-usage')
    #         options.add_argument("--proxy-bypass-list=*")

    #         # Set other headers
    #         for header, value in headers.items():
    #             options.add_argument(f"{header}: {value}")

    #         chrome_prefs = {
    #             "profile.default_content_settings": {"images": 2},
    #             "profile.managed_default_content_settings": {"images": 2},
    #         }

    #         options.add_experimental_option("prefs", chrome_prefs)

    #         try:
    #             service = Service(ChromeDriverManager().install())
    #             driver = webdriver.Chrome(options=options, service=service)
    #             print('here')
    #         except Exception as e:
    #             service = Service(os.path.join(os.getcwd(), './app/scraper/chromedrivers/chromedriver111'))
    #             driver = webdriver.Chrome(options=options, service=service)

    #         return driver
    #     except Exception as e:
    #         return None

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError(
            "Abstract method 'run' must be implemented in subclass.")

    def _validate_unique_jobs(self, jobs: list) -> list:
        return jobs

    def save(self, runner, jobs: list) -> None:
        print('Save called!', jobs)
        pass
