import requests
from bs4 import BeautifulSoup
import re

class IIHS:

    def __init__(self):
        page = requests.get("https://www.iihs.org/ratings/top-safety-picks")
        self.soup = BeautifulSoup(page.content, "html.parser")
        rawCards = self.soup.find_all("a", class_="card")
        self.iihsPicks = {}
        for card in rawCards:
            content = card.find("div", class_="card-content").find_all("p")
            brokenModel = re.split(r"([0-9]-door)", content[1].contents[0].strip())
            if len(brokenModel) == 3:
                spec = brokenModel[1] + brokenModel[2]
            pick = ""
            if content[0].attrs["class"][1] == "tspBanner":
                pick = "IIHS Top Safety Pick"
            else:
                pick = "IIHS Top Safety Pick+"
            if len(content[2].contents) == 1:
                spec += " " + content[2].contents[0]
            self.iihsPicks[brokenModel[0].strip().lower()] = {
                "selection": pick,
                "details": spec
            }

    def findDep(self, make, model, year):
        car = f"{year} {make} {model}"
        if car in self.iihsPicks:
            return self.iihsPicks[car]
        else:
            return  "N/A"
