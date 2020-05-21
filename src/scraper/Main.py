from Fish import Fish
from FishScraper import FishScraper
from FishSQLConnector import FishSQLConnector

fishHtmlFileName = "../../resources/acnh-fish.html"
fishDocument = open(fishHtmlFileName,"r")
fishHtml = fishDocument.read()
fishDocument.close()
fishScraper = FishScraper(fishHtml)

fishSQLConnector = FishSQLConnector("root", "nooky")
fishSQLConnector.populate(fishScraper.fishes)
fishSQLConnector.close()
