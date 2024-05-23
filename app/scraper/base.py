from abc import abstractmethod
import os
import ast

from app.scraper.constants import headers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Script:

    def __init__(self) -> None:
        self.keywords = ['Python']
        self.locations = []

    def get_headers(self):
        print('Headers called!')
        return headers

    def get_options(self):
        print('Options called!')
        try:

            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-infobars")
            options.add_argument("--no-sandbox")
            # options.add_argument("--headless") # Comment this our for testing
            options.add_argument("--lang=en-US")
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--start-maximized')
            options.add_argument("--proxy-server='direct://'")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--proxy-bypass-list=*")

            # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Set other headers
            for header, value in headers.items():
                options.add_argument(f"{header}: {value}")

            chrome_prefs = {
                "profile.default_content_settings": {"images": 2},
                "profile.managed_default_content_settings": {"images": 2},
            }

            options.add_experimental_option("prefs", chrome_prefs)

            service = Service(executable_path=ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # driver = webdriver.Remote(command_executor='https://jobs-scraper-default.up.railway.app', options=options)

            return driver
        except Exception as exc:
            print('Options ERROR:', str(exc))
            return None

    def update_runner(self, runner) -> None:
        print('Updated Runner called!')

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError(
            "Abstract method 'run' must be implemented in subclass.")

    def _validate_unique_jobs(self, jobs: list) -> list:
        return jobs

    def save(self, runner, jobs: list) -> None:
        print('Save called!')
        jobs = self._validate_unique_jobs(jobs=jobs)
        jobs_bulk = []
        try:
            print('JOBS:', jobs)
        except Exception as exc:
            print(f'Exception on save:{runner}:', str(exc))
