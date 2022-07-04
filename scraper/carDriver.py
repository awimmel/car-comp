import requests
from bs4 import BeautifulSoup
import re
import csv

class CarDriver:

    cars = []

    def __init__(self, make, model, year):
        correctModel = model
        if model.startswith("mazda"):
            correctModel = re.split(r"mazda", model)[1]
        self.make = make
        self.model = correctModel
        self.year = year
        url = f"https://www.caranddriver.com/{make}/{correctModel}"
        if year != "2022":
            url += f"-{year}"
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.overallScore = 0
        self.pros = ""
        self.cons = ""
        self.overallEval = ""
        self.rank = 0

    def readPage(self):
        scoreResult = self.soup.find("span", class_="css-7a3l6c e91pesh2")
        self.overallScore = float(scoreResult.contents[0])
        detComments = self.soup.find("ul", class_="css-17qs78k e18q3jx02").find_all("li")
        self.pros = detComments[0].contents[2]
        self.cons = detComments[1].contents[1]
        self.overallEval = detComments[2].contents[1]
        rankEl = self.soup.find("div", class_="css-czi23h")
        self.rank = int(rankEl.contents[0])
        CarDriver.cars.append(self)
    
    def genCSV():
        with open('data/carDriver.csv', 'w', newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Overall Score", "Pros", "Cons", "Overall Eval.", "Rank"]
            writer.writerow(header)
            for car in CarDriver.cars:
                currentRow = [car.make, car.model, car.year, car.overallScore, car.pros, car.cons, car.overallEval, car.rank]
                writer.writerow(currentRow)

