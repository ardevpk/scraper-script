
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from app.scraper.base import Script


class CustomScraper(Script):

    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://www.ziprecruiter.com"
        self.job_portal = "https://www.ziprecruiter.com/candidate/search?radius=5000&days=5&search={}&location={}"
        self.locations = ['Pennsylvania', 'Florida', 'Georgia', 'Texas']
        # self.keywords = ['Python', 'Django', 'Flask', 'FastAPI']

    def _get_jobs(self, job_collection):
        jobs = []
        for main_div in job_collection:
            try:
                try:
                    company = main_div.find(
                        'p', {"class": "text-black normal-case line-clamp-1 text-body-md"}).a.text.split()
                    company = company[0]
                except:
                    company = None

                try:
                    job_url = main_div.find(
                        "h2", {"class": "font-bold text-black text-header-sm"})
                    if job_url:
                        anchor_tag = job_url.find("a")
                        if anchor_tag and 'href' in anchor_tag.attrs:
                            job_url = urljoin(
                                self.base_url, anchor_tag['href'])
                        else:
                            print(
                                "Anchor tag with href attribute not found within the h2 element.")
                    else:
                        print("h2 element with specified class not found.")

                    # job_url = urljoin(self.base_url, job_url)
                except:
                    job_url = None
                try:
                    salary = main_div.find(
                        "div", {"class": "mr-8"}).text.strip()
                except:
                    salary = None
                try:
                    title = main_div.find(
                        "h2", {"class": "font-bold text-black text-header-sm"}).text.strip()
                except:
                    title = None
                try:
                    location = main_div.find(
                        'p', {'class': "text-black normal-case text-body-md"}).text.strip()
                except:
                    location = None
                try:
                    City = location.split()[0]
                except:
                    City = location
                try:
                    State = location.split()[2]
                except:
                    State = None

                country = " "
                try:
                    posted_date = 'Today'
                except:
                    posted_date = None
                current_item = {
                    "name": title,
                    "link": job_url,
                    "description": {
                        "Company": company,
                        "City": City,
                        "State": State,
                        "Platform": "ZipRecuiter",
                        "Posted_date": posted_date,
                        "Region": country,
                        "Salary": salary,
                    }
                }
                jobs.append(current_item)
            except Exception as exc:
                print("Error in HTML Code", exc)
                continue
        return jobs

    def us_main_code(self, runner):
        driver = self.get_options()

        for location in self.locations:
            location = location.replace(" ", "+")
            for keyword in self.keywords:
                keyword = keyword.replace(" ", '+')
                try:
                    pg = 0
                    end = 1
                    keyword = keyword.replace('/', '%2F')
                    while pg < end:
                        pg += 1
                        url = self.job_portal.format(keyword, location)
                        print('URL:', url)

                        driver.get(url)
                        driver.implicitly_wait(10)
                        time.sleep(3)
                        
                        from selenium.webdriver.common.by import By
                        from selenium.webdriver.support.ui import WebDriverWait
                        from selenium.webdriver.support import expected_conditions as EC

                        def check_cloudflare_and_solve(driver):
                            try:
                                # Wait for Cloudflare challenge to be visible
                                for wait in range(5, 20, 5):
                                    print('Cloudflare wait:', wait)
                                    cloudflare_challenge = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.ID, "cf-challenge-running"))
                                    )
                                    if cloudflare_challenge:
                                        print("Cloudflare challenge detected, waiting for it to complete...")
                                        time.sleep(wait)  # Adjust sleep time as necessary for the challenge to complete
                                        return True
                                    return False
                            except Exception as exc:
                                print("No Cloudflare challenge detected:", str(exc))
                                return False

                        def wait_for_class(driver, class_name):
                            try:
                                element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                                )
                                return element
                            except:
                                return None

                        desired_class = 'job_result_wrapper'
                        element = wait_for_class(driver, desired_class)
                        # If the class is not present, check for Cloudflare challenge
                        if not element:
                            cloudflare_solved = check_cloudflare_and_solve(driver)
                            if cloudflare_solved:
                                # After waiting for Cloudflare challenge, check for the desired class again
                                element = wait_for_class(driver, desired_class)
                                # time.sleep(10)

                                soup = BeautifulSoup(driver.page_source, "html.parser")
                                try:
                                    job_collection = soup.findAll("div", {"class": "job_result_wrapper"})
                                    # job_collection = soup.findAll("div", {"class": "mb-12 flex flex-col gap-12"})
                                    if len(job_collection) != 0:
                                        jobs = self._get_jobs(job_collection)
                                        self.save(runner=runner, jobs=jobs)
                                    else:
                                        driver.save_screenshot('./screenshot.png')
                                        print('Screenshot Saved!')
                                        break
                                except Exception as exc:
                                    print("Error in Get JOB Function", exc)
                                    break
                            else:
                                print('Cloudflare challeng failed!')
                except:
                    print("Error in Url")
                    continue
        driver.quit()

    def run(self, runner):
        try:
            self.us_main_code(runner=runner)
        except Exception as exc:
            print('Zip Recruiter Exception:', exc)



if __name__ == "__main__":
    scraper = CustomScraper()
    scraper.run(runner=0.1)
