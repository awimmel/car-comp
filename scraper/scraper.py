from cr import ConsRep
from edmunds import Edmunds
from iiihs import IIHS
from jdp import JDPower
from kbb import KBB
from carDriver import CarDriver
from motortrend import MotorTrend
from carEdge import CarEdge
from usNews import USNews
from car import Car
from car import Site
import csv



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
        currentCar = Car(make, model, year, carAndDriver, edmunds, jdp, kbb, motortrend, usNews)
        scrapePages(currentCar)
        cars.append(currentCar)

        choice = input("Enter x to quit and generate CSVs. Enter any other key to continue: ")
    
    
    genCSV(cars)
    

def scrapePages(car):
    for site in car.sites:
        car.sites[site].readPage()
    
def genCSV(cars):
    carEdge = CarEdge()
    cr = ConsRep()
    iihs = IIHS()
    with open('data/main.csv', 'w', newline="", encoding="UTF8") as file:
        writer = csv.writer(file)
        header = ["Make", "Model", "Year", "MSRP", "Fair Price", "Priced Version", "MPG (City)", "MPG (Hwy)",
            "Horsepower", "Transmission", "Engine", "Drivetrain", "Car and Driver Review", "Edmunds Critic", "Edmunds User",
            "JDP Score", "JDP Rank", "KBB Critic", "KBB User", "Motortrend Score", "Motortrend Ranking", "US News",
            "JDPower Relaibility (Probs./100 vehicles)", "CR Reliability Score", "CR Reliability Rank", "5-Year Depreciation", "IIHS Designation", "IIHS Addit'l Info"]
        writer.writerow(header)
        for car in cars:
            currentIIHS = iihs.findDep(car.make, car.model, car.year)
            if currentIIHS == "N/A":
                currentIIHS = {
                    "selection": "N/A",
                    "details": "N/A"
                }
            currentRow = [car.make, car.model, car.year, car.sites[Site.MOTORTREND].price["msrp"],
                car.sites[Site.MOTORTREND].price["fairPrice"],car.sites[Site.MOTORTREND].price["version"],
                car.sites[Site.JDP].spec["mpgCity"], car.sites[Site.JDP].spec["mpgHwy"], car.sites[Site.JDP].spec["horsepower"],
                car.sites[Site.JDP].spec["transmission"], car.sites[Site.JDP].spec["engine"], car.sites[Site.JDP].spec["drivetrain"],
                car.sites[Site.CAR_DRIVER].overallScore, car.sites[Site.EDMUNDS].overallScore, car.sites[Site.EDMUNDS].consumScore,
                car.sites[Site.JDP].overall, car.sites[Site.JDP].rank, car.sites[Site.KBB].expertScore, car.sites[Site.KBB].userScore,
                car.sites[Site.MOTORTREND].score, car.sites[Site.MOTORTREND].ranking, car.sites[Site.US_NEWS].overall, car.sites[Site.JDP].reliability,
                cr.reliability(car.make)["score"], cr.reliability(car.make)["ranking"], carEdge.findDep(car.make), currentIIHS["selection"], currentIIHS["details"]]
            writer.writerow(currentRow)
    CarDriver.genCSV()
    Edmunds.genCSV()
    JDPower.genCSV()
    KBB.genCSV()
    MotorTrend.genCSV()
    USNews.genCSV()

if __name__ == '__main__':
    readAndAct()

