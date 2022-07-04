import requests
from bs4 import BeautifulSoup
import re
import csv

class MotorTrend:

    cars = []
    def __init__(self, make, model, year):
        correctModel = model
        if make == "mazda" and model.isnumeric():
            correctModel = f"mazda{model}"
        
        self.make = make
        self.model = correctModel
        self.year = year

        page = requests.get(f"https://www.motortrend.com/cars/{make}/{correctModel}/{year}/")
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.score = -1
        self.ranking = -1
        self.price = {
            "version": "N/A",
            "msrp": "N/A",
            "fairPrice": "N/A"
        }
        self.perf = -1
        self.eff = -1
        self.tech = -1
        self.value = -1
    
    def readPage(self):
        try:
            scoreResult = self.soup.find("span", class_="_2bK3N")
            self.score = float(re.sub(r"/10", "", scoreResult.contents[0]))

            rankingResult = self.soup.find("div", class_="_616_M")
            self.ranking = int(re.split("#|\W",rankingResult.contents[0])[1])

            trimRes = self.soup.find("div", class_="_2spOl")
            self.price["version"] = trimRes.contents[0]
            self.price["msrp"] = self.soup.find("table", class_="HgJzJ _3UC6i _2T0d8").find_all("td")[1].contents[0]
            self.price["fairPrice"] = self.soup.find("table", class_="HgJzJ _3UC6i _2T0d8").find_all("td")[2].contents[0]

            detScoreRes = self.soup.find_all("span", class_="_3N0CY")
            self.perf = detScoreRes[0].contents[0]
            self.eff = detScoreRes[1].contents[0]
            self.tech = detScoreRes[2].contents[0]
            self.value = detScoreRes[3].contents[0]
            MotorTrend.cars.append(self)
        except AttributeError:
            print("Error reading MotorTrend. Please enter a different make, model, or year.")

    def genCSV():
        with open('data/motortrend.csv', 'w', newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Overall Score", "Performance Score", "Efficiency Score",
            "Technology Score", "Value Score", "Ranking", "MSRP", "Fair Price", "Model Version for Prices"]
            writer.writerow(header)
            for car in MotorTrend.cars:
                currentRow = [car.make, car.model, car.year, car.score, car.perf, car.eff, car.tech, car.value,
                    car.ranking, car.price["msrp"], car.price["fairPrice"], car.price["version"]]
                writer.writerow(currentRow)

