from abc import abstractmethod
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth


from app.scraper.constants import user_agents


class Script:

    def __init__(self) -> None:
        self.runner: str
        self.keywords = ['Python']
        self.logger: str

    def get_headers(self):
        print('Headers called!')
        headers = {
            'user-agent': random.choice(user_agents),
        }
        return headers

    def get_options(self):
        print('Options called!')
        driver = None
        try:

            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-infobars")
            # options.add_argument("--headless")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--lang=en-US")
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--start-maximized')
            options.add_argument("--proxy-server='direct://'")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--proxy-bypass-list=*")

            options.add_argument("--no-sandbox")
            # disable shared memory usage
            options.add_argument('--disable-dev-shm-usage')

            # Set other headers
            for header, value in self.get_headers().items():
                options.add_argument(f"{header}={value}")

            chrome_prefs = {
                "profile.default_content_settings": {"images": 2},
                "profile.managed_default_content_settings": {"images": 2},
            }

            options.add_experimental_option("prefs", chrome_prefs)

            service = Service(executable_path=ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            # stealth(driver,
            #     languages=["en-US", "en"],
            #     vendor="Google Inc.",
            #     platform="Win32",
            #     webgl_vendor="Intel Inc.",
            #     renderer="Intel Iris OpenGL Engine",
            #     fix_hairline=True,
            # )

            return driver

        except Exception as exc:
            print('Options ERROR:', str(exc))
            self.add_logs(desc=f'Options ERROR: {str(exc)}')

            if driver is not None:
                driver.quit()

            return None

    def init_logger(self):
        pass

    def update_runner(self, runner: str) -> None:
        print('Updated Runner called!')
        self.init_logger()
        pass

    def add_logs(self, desc: str = ''):
        """
        Example:
        add_logs(desc='Error in url, Example error message to save in runner logs')
        """
        pass

    def save_image_in_db(self, png_bytes):
        """
        Example:
        save_image_in_db(driver.get_screenshot_as_png())
        Use driver.get_screenshot_as_png() function that return byte code or bytes
        of that PNG!
        And that will be later on saved in DB with a specific runner object!
        """
        pass

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError(
            "Abstract method 'run' must be implemented in subclass.")

    def _validate_unique_jobs(self, jobs: list) -> list:
        return jobs

    def save(self, jobs: list) -> None:
        print('Save called!')
        jobs = self._validate_unique_jobs(jobs=jobs)
        try:
            print('JOBS:', jobs)
            """
            Here jobs will be saved in DB! With bulk DB operation!
            """
        except Exception as exc:
            print(f'Exception on save:{self.runner}:', str(exc))
            self.add_logs(desc=f'Exception on save: {str(exc)}')
