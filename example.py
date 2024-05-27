
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
                print("Error in HTML Code:", str(exc))
                self.add_logs(desc=f'Error in HTML Code: {str(exc)}')
        return jobs

    def us_main_code(self):
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
                        time.sleep(5)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        try:
                            job_collection = soup.findAll("div", {"class": "job_result_wrapper"})
                            if len(job_collection) != 0:
                                jobs = self._get_jobs(job_collection)
                                self.save(jobs=jobs)
                            else:
                                self.save_image_in_db(png_bytes=driver.get_screenshot_as_png())
                                break
                        except Exception as exc:
                            print("Error at Get JOB Function:", str(exc))
                            self.add_logs(desc=f'Error at Get JOB Function:{url}: {str(exc)}')
                            break
                except Exception as exe:
                    print("Error in loop:", str(exe))
                    self.add_logs(desc=f'Error in loop: {str(exe)}')
                    continue
        driver.quit()

    def run(self):
        try:
            self.us_main_code()
        except Exception as exc:
            print('Zip Recruiter Exception:', exc)


if __name__ == '__main__':
    script = CustomScraper()
    script.run()
