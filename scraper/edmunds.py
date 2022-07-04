import requests
from bs4 import BeautifulSoup
import csv

class Edmunds:

    cars = []

    def __init__(self, make, model, year): 
        self.make = make
        self.model = model
        self.year = year

        userAgent = {
            "User-Agent": "Mozilla/5.0"
        }
        page = requests.get(f"https://www.edmunds.com/{make}/{model}/{year}/review/", headers=userAgent)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.overallScore = 0
        self.consumScore = 0
        self.perf = 0
        self.comf = 0
        self.int = 0
        self.tech = 0
        self.stor = 0
        self.fuel = 0
        self.value = 0
        self.wildcard = 0
        self.comments = [[], [], []]

    def readPage(self):
        overallScoreResult = self.soup.find("span", class_="size-40 font-weight-bold text-primary-darker")
        self.overallScore = float(overallScoreResult.contents[0])
        
        consumScoreResult = self.soup.find("div", class_="d-inline-block font-weight-bold text-gray-darker mr-0_25 mr-md-0_5 size-24")
        self.consumScore = float(consumScoreResult.contents[2])
        
        detScores = self.soup.find_all("div", class_="heading-3 text-primary-darker")
        self.perf = detScores[0].contents[0]
        self.comf = detScores[1].contents[0]
        self.int = detScores[2].contents[0]
        self.tech = detScores[3].contents[0]
        self.stor = detScores[4].contents[0]
        self.fuel = detScores[5].contents[0]
        self.value = detScores[6].contents[0]
        self.wildcard = detScores[7].contents[0]

        detCommentResult = self.soup.find_all("ul", class_="list-unstyled mb-0")
        currentInd = 0
        for group in detCommentResult:
            comments = group.find_all("span", class_="text-gray-darker")
            for comment in comments:
                self.comments[currentInd].append(comment.contents[1])
            currentInd += 1
        Edmunds.cars.append(self)

        
    def genCSV():
        with open('data/edmunds.csv', 'w',  newline="", encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Overall Score", "Consumer Score", "Performance Rating",
                "Comfort Rating", "Interior Rating", "Technology Rating", "Storage Rating", "Fuel Rating",
                "Value Rating", "Wildcard Rating", "Pros", "Cons", "What's New"]
            writer.writerow(header)
            for car in Edmunds.cars:
                currentRow = [car.make, car.model, car.year, car.overallScore, car.consumScore, car.perf,
                    car.comf, car.int, car.tech, car.stor, car.fuel, car.value, car.wildcard, car.comments[0],
                    car.comments[1], car.comments[2]]
                writer.writerow(currentRow)