import requests
from bs4 import BeautifulSoup
import csv

class KBB:

    cars = []

    def __init__(self, make, model, year):
        correctModel = model
        if make == "mazda" and model.isnumeric():
            correctModel = f"mazda{model}"
        
        self.make = make
        self.model = correctModel
        self.year = year

        page = requests.get(f"https://www.kbb.com/{make}/{correctModel}/{year}")
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.expertScore = 0
        self.userScore = 0
        self.comments = {
            "pros": [],
            "cons": [],
            "new": []
        }

    def readPage(self):
        expertResult = self.soup.find("div", class_="css-18492h9-ShortHandStarRatingXSmall")
        self.expertScore = float(expertResult.find("div").contents[0])

        userResult = self.soup.find_all("div", class_="css-18492h9-ShortHandStarRatingXSmall")[1]
        self.userScore = float(userResult.find("div").contents[0])

        detResult = self.soup.find_all("div", class_="css-180tk1l-ColBase e1l0ytpk0")
        key = "pros"
        for detail in detResult:
            comments = detail.find_all("li")
            for comment in comments:
                self.comments[key].append(comment.contents[0])
            key = "cons"
        newFeats = self.soup.find("div", "css-1ob8w23-ColBase e1l0ytpk0").find_all("li")
        for feat in newFeats:
            self.comments["new"].append(feat.contents[0])
        KBB.cars.append(self)

    def genCSV():
        with open('data/kbb.csv', 'w', encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Critic Score", "User Score", "Pros", "Cons", "New Features"]
            writer.writerow(header)
            for car in KBB.cars:
                currentRow = [car.make, car.model, car.year, car.expertScore, car.userScore, car.comments["pros"],
                car.comments["cons"], car.comments["new"]]
                writer.writerow(currentRow)
