import requests
from bs4 import BeautifulSoup
import re
import csv

class JDPower:
    makeReliab = {
        "kia": 145,
        "buick": 147,
        "hyundai": 148,
        "genesis": 155,
        "toyota": 158,
        "lexus": 159,
        "porsche": 162,
        "dodge": 166,
        "cadillac": 168,
        "chevrolet": 171,
        "mini": 173,
        "mazda": 179,
        "lincoln": 180,
        "mitsubishi": 183,
        "bmw": 187,
        "ford": 188,
        "gmc": 192,
        "mercedez-benz": 195,
        "jeep": 201,
        "nissan": 205,
        "volkswagen": 217,
        "subaru": 226,
        "infiniti": 228,
        "honda": 230,
        "audi": 232,
        "jaguar": 233,
        "chrysler": 240,
        "acura": 244,
        "alfa romeo": 245,
        "volvo": 256,
        "ram": 266,
        "land rover": 284
    }

    cars = []

    def __init__(self, make, model, year):
        correctModel = model
        if make == "mazda" and model.isnumeric():
            correctModel = f"mazda{model}"
        self.make = make
        self.model = correctModel
        self.year = year
        self.reliability = ""
        if self.make in JDPower.makeReliab:
            self.reliability = JDPower.makeReliab[self.make]
        else:
            self.reliability = "N/A"
        page = requests.get(f"https://www.jdpower.com/cars/{year}/{make}/{correctModel}")
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.overall = 0
        self.detScores = {
            "qualRel": "N/A",
            "drivExp": "N/A",
            "resale": "N/A",
            "dealer": "N/A"
        }
        self.rank = 0
        self.detRemarks = {
            "pros": [],
            "cons": []
        }
        self.spec = {
            "mpgCity": "N/A",
            "mpgHwy": "N/A",
            "horsepower": "N/A",
            "transmission": "N/A",
            "engine": "N/A",
            "drivetrain": "N/A"
        }
    
    def readPage(self):
        overallResult = self.soup.find("div", class_="radialBar_small-rating-value__Xl32u jss14 jss11")
        if overallResult is not None:
            self.overall = float(overallResult.contents[0])
            
            detResult = self.soup.find_all("span", class_="bh-m")
            self.detScores["qualRel"] = int(detResult[1].contents[0])
            self.detScores["drivExp"] = int(detResult[2].contents[0])
            self.detScores["resale"] = int(detResult[3].contents[0])
            self.detScores["dealer"] = int(detResult[4].contents[0])
            
            rankNumbResult = self.soup.find_all("div", class_="ranking-row-left bh-m")
            properResult = ""
            for result in rankNumbResult:
                if result.contents[0].startswith("#"):
                    properResult = result.contents[0]
                    break
            self.rank =int(re.split("#|\W", properResult)[1])
            
            prosConsResult = self.soup.find_all("ul", class_="discription-list jss39")
            currentList = "pros"
            for list in prosConsResult:
                entries = list.find_all("li")
                for entry in entries:
                    self.detRemarks[currentList].append(entry.contents[1])
                currentList = "cons"
        else:
            self.overall = "Not Rated"
        
        perfCont = self.soup.find("div", class_="performanceSpecs_performance-specs-wrapper__30SE9")
        specResult = perfCont.find_all("div", class_="spacing-s") 
        for spec in specResult:
            brokenKey = spec.find("h3").contents[0].split()
            brokenKey[0] = brokenKey[0].lower()
            key = brokenKey[0]
            if len(brokenKey) > 1:
                key = brokenKey[0] + brokenKey[1]            
            value = spec.find("p", class_="bh-m spec_spec-body__1xMB0").contents[0]
            self.spec[key] = value
        JDPower.cars.append(self)

    def genCSV():
        with open('data/jdp.csv', 'w', encoding="UTF8") as file:
            writer = csv.writer(file)
            header = ["Make", "Model", "Year", "Overall Score", "Quality and Reliability",
                "Driving Experience", "Resale", "Dealership Experience", "Rank", "Pros", "Cons", "Reliability (Probs./100 vehicles)",
                "City MPG", "Hwy MPG", "Horsepower", "Transmission", "Engine", "Drivetrain"]
            writer.writerow(header)
            for car in JDPower.cars:
                currentRow = [car.make, car.model, car.year, car.overall, car.detScores["qualRel"],
                    car.detScores["qualRel"], car.detScores["drivExp"], car.detScores["resale"], car.detScores["dealer"],
                    car.rank, car.detRemarks["pros"], car.detRemarks["cons"], car.spec["mpgCity"], car.spec["mpgHwy"],
                    car.spec["horsepower"], car.spec["transmission"], car.spec["engine"], car.spec["drivetrain"]]
                writer.writerow(currentRow)

