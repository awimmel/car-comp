import requests
from bs4 import BeautifulSoup

class ConsRep:

    def __init__(self):
        page = requests.get("https://www.kbb.com/car-news/consumer-reports-lexus-makes-the-most-reliable-cars-lincoln-the-least/")
        self.soup = BeautifulSoup(page.content, "html.parser")
        rows = self.soup.find("table").find_all("tr")
        self.relValues = {}
        skip = True
        for row in rows:
            columns = row.find_all("td")
            if len(columns) == 3 and not skip:
                self.relValues[columns[1].contents[0].lower()] = {
                    "ranking": columns[0].contents[0],
                    "score": columns[2].contents[0]
                }
            skip = False

    def reliability(self, make):
        if make in self.relValues:
            return self.relValues[make]
        else:
            return {
                "ranking": "N/A",
                "score": "N/A"
            }
