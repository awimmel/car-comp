import requests
from bs4 import BeautifulSoup
import csv

class USNews:

    cars = []

    def __init__(self, make, model, year):
        correctModel = model
        if make == "mazda" and model.isnumeric():
            correctModel = f"mazda{model}"

        self.make = make
        self.model = correctModel
        self.year = year

        userAgent = {
            "User-Agent": "Mozilla/5.0"
        }
        page = requests.get(f"https://cars.usnews.com/cars-trucks/{make}/{correctModel}/{year}", headers=userAgent)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.overall = -1
        self.comments = {
            "pros": ["N/A"],
            "cons": ["N/A"]
        }
        self.critics = -1
        self.perf = -1
        self.int = -1
        self.safety = -1
        self.qual = -1

    def readPage(self):
        try:
            overallResult = self.soup.find("p", class_="scorecard__score")
            self.overall = float(overallResult.contents[0])

            prosRes = self.soup.find("div", class_="pros").find_all("li")
            self.comments["pros"] = []
            for pro in prosRes:
                self.comments["pros"].append(pro.contents[0])
            consRes = self.soup.find("div", class_="cons").find_all("li")
            self.comments["cons"] = []
            for con in consRes:
                self.comments["cons"].append(con.contents[0])
            

            subscoreRes = self.soup.find_all("td", class_="float-right item scorecard__value-label")
            self.critics = float(subscoreRes[0].contents[1])
            self.perf = float(subscoreRes[1].contents[1])
            self.int = float(subscoreRes[2].contents[1])
            self.safety = float(subscoreRes[3].contents[1])
            USNews.cars.append(self)
        except AttributeError:
            print("Error reading U.S. News & World Report. Please enter a different make, model, or year.")

    def genCSV():
        with open('data/usNews.csv', 'w', newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Overall Score", "Critics Score", "Performance Score", "Interior Score",
            "Safety Score", "Quality Score", "Pros", "Cons"]
            writer.writerow(header)
            for car in USNews.cars:
                currentRow = [car.make, car.model, car.year, car.overall, car.critics, car.perf, car.int,
                    car.safety, car.qual, car.comments["pros"], car.comments["cons"]]
                writer.writerow(currentRow)

