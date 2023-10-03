from bs4 import BeautifulSoup


TECHNOLOGIES_LIST = [
    "Django", "Flask", "SQLAlchemy", "Pandas", "NumPy",
    "SciPy", "Matplotlib", "Django REST Framework", "Celery",
    "Redis", "RabbitMQ", "Docker", "AWS", "Heroku", "PostgreSQL",
    "MySQL", "MongoDB", "REST", "Python", "Git", "API", "Fast API",
    "asyncio", "SQL", "linux", "Machine Learning", "Artificial intelligence",
    "JS", "OOP", "react", "networking", "fullstack", "HTML", "CSS", "GraphQl",
    "Java"
]


def find_technologies(soup: BeautifulSoup) -> list[str]:
    technologies = []
    description = (
        soup.select_one(".job-list-item__description > span")
        ["data-original-text"]
    )
    for tech in TECHNOLOGIES_LIST:
        if tech.lower() in description.lower():
            technologies.append(tech)
    return technologies
