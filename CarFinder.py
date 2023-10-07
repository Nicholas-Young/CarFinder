from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
botContext = []

@bot.event
async def on_ready():
    print("I'm ready to go!")

@bot.command()
async def start(ctx, *args):
    botContext.append(ctx)
    message = "Channel subscribed. Updates will now be posted!"
    await ctx.send(message)
    carfinder = CarFinder()
    while(True):
        print("Running all checks... (" + str(datetime.now()) + ")")
        await carfinder.newbrowser()
        await carfinder.checkAll()
        time.sleep((59 - datetime.now().minute) * 60 + (60 - datetime.now().second)) #Run at the top of every hour

async def sendBotAlert(msg):
    for ctx in botContext:
        await ctx.send(msg)

class CarFinder:
    def __init__(self):
        self.executable = '<PATH TO geckodriver.exe>' #Path to executable removed for privacy
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--headless")
        self.knownCars = {}
        self.browser = self.newbrowser()

    async def newbrowser(self):
        self.browser = webdriver.Firefox(executable_path = self.executable, options=self.options)

    async def sendAlert(self, model, dealership):
        await sendBotAlert("New " + model + " at " + dealership + "!!!")

    async def checkAll(self):
        print("\tRunning checks...")
        await self.parseVehicles(await self.getVehicles("<URL HERE>", "stock", "A"), self.parseA, "A") #URL and location names removed for privacy
        await self.parseVehicles(await self.getVehicles("<URL HERE>", "vin-row", "B"), self.parseB, "B") #URL and location names removed for privacy
        await self.parseVehicles(await self.getVehicles("<URL HERE>", "stock-row", "C"), self.parseC, "C") #URL and location names removed for privacy
        await self.parseVehicles(await self.getVehicles("<URL HERE>", "stock-row", "D"), self.parseD, "D") #URL and location names removed for privacy
        print("\tFinished checks...")

    async def getVehicles(self, url, classname, name=""):
        print("\tChecking " + name)
        self.browser.get(url)
        return self.browser.find_elements(by=By.CLASS_NAME, value=classname)

    async def parseVehicles(self, vehicles, parse, name, model="vehicle"):
        for vehicle in vehicles:
            idNum = await parse(vehicle)
            if name not in self.knownCars.keys():
                self.knownCars[name] = []
            if idNum not in self.knownCars[name]:
                self.knownCars[name].append(idNum)
                await self.sendAlert(model, name)

    #Need some kind of parsing function for each website to grab some kind of vehicle ID like VIN or Stock Number
    async def parseA(self, vehicle):
        return vehicle.text

    async def parseB(self, vehicle):
        return vehicle.text[5:]

    async def parseC(self, vehicle):
        return vehicle.text[7:]

    async def parseD(self, vehicle):
        return vehicle.text[8:]

if __name__ == "__main__":
    bot.run('BOT KEY HERE') #Bot key removed for security