import csv
import os
from dataclasses import dataclass, fields
import requests
from bs4 import BeautifulSoup
from scraping.config import find_technologies

BASE_URL = "https://djinni.co/jobs/?primary_keyword=Python"


@dataclass
class Jobs:
    vacancy_name: str
    company: str
    years_of_experience: str
    technologies: list[str]


FIELD_NAMES = [field.name for field in fields(Jobs)]


def parse_single_job(soup: BeautifulSoup) -> Jobs:
    return Jobs(
        vacancy_name=soup.select_one(".h3.job-list-item__link").text,
        company=soup.select_one("a.mr-2").text,
        years_of_experience=soup.select_one(
            ".job-list-item__job-info > span:-soup-contains('experience')"
        ).text,
        technologies=find_technologies(soup)
    )


def get_page_num(soup: BeautifulSoup) -> int:
    page_soup = soup.select_one(".pagination ")
    if page_soup is None:
        return 1
    return int(page_soup.select("li")[-2].text)


def get_single_job(soup: BeautifulSoup) -> [Jobs]:
    jobs = soup.select(".job-list-item")
    return [parse_single_job(job_soup) for job_soup in jobs]


def main(output_csv_path: str) -> None:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    num_pages = get_page_num(soup)
    all_jobs = get_single_job(soup)

    # for page_num in range(2, num_pages + 1):
    #     page = requests.get(BASE_URL, {"page": page_num}).content
    #     soup = BeautifulSoup(page, "html.parser")
    #     all_jobs.extend(get_single_job(soup))

    with open(output_csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(FIELD_NAMES)
        for job in all_jobs:
            writer.writerow(
                [
                    job.vacancy_name,
                    job.company,
                    job.years_of_experience,
                    job.technologies
                ]
            )


if __name__ == "__main__":
    main(os.path.join("..", "jobs.csv"))
    print("Done!")
