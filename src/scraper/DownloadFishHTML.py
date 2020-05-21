import requests

fishUrl = 'https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)'
fishResponse = requests.get(fishUrl)
fishDocumentName = '../resources/acnh-fish.html'
fishDocument = open(fishDocumentName, 'w')
fishDocument.write(fishResponse.text)
fishDocument.close()

