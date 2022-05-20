import requests
from bs4 import BeautifulSoup

class CarEdge:

    def __init__(self):
        page = requests.get("https://caredge.com/ranks/depreciation/popular/5-year/best")
        self.soup = BeautifulSoup(page.content, "html.parser")
        rows = self.soup.find("table").find_all("tr")
        self.depValues = {}
        for row in rows:
            columns = row.find_all("td")
            if len(columns) == 3:
                self.depValues[columns[1].find("a").contents[0].lower()] = columns[2].contents[0]

    def findDep(self, make):
        if make in self.depValues:
            return self.depValues[make]
        else:
            return  "N/A"
