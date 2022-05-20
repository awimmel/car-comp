from cr import ConsRep
from edmunds import Edmunds
from iiihs import IIHS
from jdp import JDPower
from kbb import KBB
from carDriver import CarDriver
from motortrend import MotorTrend
from carEdge import CarEdge
from usNews import USNews
from enum import Enum
import csv

class Site(Enum):
    CAR_DRIVER = 1
    EDMUNDS = 2
    JDP = 3
    KBB = 4
    MOTORTREND = 5
    US_NEWS = 6

def readAndAct():
    choice = ""
    cars = []
    while choice != "x":
        make = input("Make: ").lower()
        model = input("Model: ").lower()
        year = input("Year: ").lower()
        carAndDriver = CarDriver(make, model, year)
        edmunds = Edmunds(make, model, year)
        jdp = JDPower(make, model, year)
        kbb = KBB(make, model, year)
        motortrend = MotorTrend(make, model, year)
        usNews = USNews(make, model, year)
        currentCar = {
            "make": make,
            "model": model,
            "year": year,
            Site.CAR_DRIVER: carAndDriver,
            Site.EDMUNDS: edmunds,
            Site.JDP: jdp,
            Site.KBB: kbb,
            Site.MOTORTREND: motortrend,
            Site.US_NEWS: usNews
        }
        scrapePages(currentCar)
        cars.append(currentCar)

        choice = input("Enter x to quit and generate CSVs. Enter any other key to continue: ")
    genCSV(cars)
    

def scrapePages(car):
    for site in car:
        if site not in ["make", "model", "year"]:
            car[site].readPage()
    
def genCSV(cars):
    carEdge = CarEdge()
    cr = ConsRep()
    iihs = IIHS()
    with open('data/main.csv', 'w', encoding="UTF8") as file:
        writer = csv.writer(file)
        header = ["Make", "Model", "Year", "MSRP", "Fair Price", "Priced Version", "MPG (City)", "MPG (Hwy)",
            "Horsepower", "Transmission", "Engine", "Drivetrain", "Car and Driver Review", "Edmunds Critic", "Edmunds User",
            "JDP Score", "JDP Rank", "KBB Critic", "KBB User", "Motortrend Score", "Motortrend Ranking", "US News",
            "JDPower Relaibility (Probs./100 vehicles)", "CR Reliability Score", "CR Reliability Rank", "5-Year Depreciation", "IIHS Designation", "IIHS Addit'l Info"]
        writer.writerow(header)
        for car in cars:
            currentIIHS = iihs.findDep(car["make"], car["model"], car["year"])
            if currentIIHS == "N/A":
                currentIIHS = {
                    "selection": "N/A",
                    "details": "N/A"
                }
            currentRow = [car["make"], car["model"], car["year"], car[Site.MOTORTREND].price["msrp"],
                car[Site.MOTORTREND].price["fairPrice"],car[Site.MOTORTREND].price["version"],
                car[Site.JDP].spec["mpgCity"], car[Site.JDP].spec["mpgHwy"], car[Site.JDP].spec["horsepower"],
                car[Site.JDP].spec["transmission"], car[Site.JDP].spec["engine"], car[Site.JDP].spec["drivetrain"],
                car[Site.CAR_DRIVER].overallScore, car[Site.EDMUNDS].overallScore, car[Site.EDMUNDS].consumScore,
                car[Site.JDP].overall, car[Site.JDP].rank, car[Site.KBB].expertScore, car[Site.KBB].userScore,
                car[Site.MOTORTREND].score, car[Site.MOTORTREND].ranking, car[Site.US_NEWS].overall, car[Site.JDP].reliability,
                cr.reliability(car["make"])["score"], cr.reliability(car["make"])["ranking"], carEdge.findDep(car["make"]), currentIIHS["selection"], currentIIHS["details"]]
            writer.writerow(currentRow)
    CarDriver.genCSV()
    Edmunds.genCSV()
    JDPower.genCSV()
    KBB.genCSV()
    MotorTrend.genCSV()
    USNews.genCSV()

if __name__ == '__main__':
    readAndAct()

