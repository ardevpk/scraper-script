
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from app.scraper.base import Script


class CustomScraper(Script):

    def __init__(self) -> None:
        super().__init__()
        self.locations = ['United States', 'New York', 'UK', 'Austria', 'UAE']
        self.base_url = "https://www.ziprecruiter.com"
        self.job_portal = "https://www.ziprecruiter.com/candidate/search?radius=5000&days=5&search={}&location={}"

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
            print(self.keywords)
            for keyword in self.keywords:
                keyword = keyword.replace(" ", '+')
                try:
                    pg = 0
                    end = 3
                    keyword = keyword.replace('/', '%2F')
                    while pg < end:
                        pg += 1
                        url = self.job_portal.format(keyword, location)
                        print(url)

                        driver.get(url)
                        driver.implicitly_wait(10)
                        time.sleep(3)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        try:
                            job_collection = soup.findAll(
                                "div", {"class": "flex flex-col gap-24 md:gap-36"})
                            if len(job_collection) != 0:
                                jobs = self._get_jobs(job_collection)
                                self.save(runner=runner, jobs=jobs)
                            else:
                                break
                        except Exception as exc:
                            print("Error in Get JOB Function", exc)
                            break
                except:
                    print("Error in Url")
                    continue
        driver.quit()

    def run(self, runner):
        try:
            self.us_main_code(runner=runner)
        except Exception as exc:
            print('Zip Recruiter Exception:', exc)

CustomScraper().run(runner=None)
