from seleniumTest import Navigator
from selenium import webdriver
import json
import copy

webdriver_url = 'http://localhost:4444/wd/hub'


firefoxOptions = webdriver.FirefoxOptions()
chromeOptions=webdriver.ChromeOptions()
edgeOptions = webdriver.EdgeOptions()

drivers = [
    firefoxOptions,
    chromeOptions,
    edgeOptions
]

sucesos = []

def executeScript(path:str, drivers:list) -> list:
    with open(path, "r", encoding='utf-8') as file:
        jsonData = json.load(file)

    tests:list = jsonData["tests"]
    url = jsonData["targetURL"]

    for t in tests:
        for driver in drivers:
            result = Navigator(command_executor=webdriver_url, options=driver)
            result.initialArguments(url=url, test=t)
            result.executeRoutine()
            if len(result.sucesos) != 0:
                sucesos.append(result.sucesos)


executeScript('filteredTests.json', drivers)

data = {
    "sucesos" : sucesos
}

#Crear JSON con sucesos
if len(sucesos) > 0:
    with open('data.json', "w", encoding='utf-') as file:
        json.dump(data, file, ensure_ascii=False)