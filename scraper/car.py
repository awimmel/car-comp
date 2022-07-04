from enum import Enum

class Site(Enum):
    CAR_DRIVER = 1
    EDMUNDS = 2
    JDP = 3
    KBB = 4
    MOTORTREND = 5
    US_NEWS = 6

class Car:
    def __init__(self, make, model, year, carDriver, edmunds, jdp, kbb, motortrend, usNews):
        self.make = make
        self.model = model
        self.year = year
        self.sites = {
            Site.CAR_DRIVER: carDriver,
            Site.EDMUNDS: edmunds,  
            Site.JDP: jdp,
            Site.KBB: kbb,
            Site.MOTORTREND: motortrend,
            Site.US_NEWS: usNews
        }