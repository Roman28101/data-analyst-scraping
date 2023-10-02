from dataclasses import dataclass, fields


from bs4 import BeautifulSoup

from scraping.config import find_technologies

BASE_URL = "https://djinni.co/jobs/?primary_keyword=Python"


@dataclass
class Jobs:
    vacancy_name: str
    company: str
    years_of_experience: int
    technologies: list[str]


FIELD_NAMES = [field.name for field in fields(Jobs)]


def parse_single_job(soup: BeautifulSoup) -> Jobs:
    return Jobs(
        vacancy_name=soup.select_one(".h3.job-list-item__link").text,
        company=soup.select_one("a.mr-2").text,
        years_of_experience=int(soup.select_one(".job-list-item__job-info > span:nth-child(4)").text.split(" ")[0]),
        technologies=find_technologies(soup)
    )
