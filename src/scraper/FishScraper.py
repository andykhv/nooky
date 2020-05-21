from bs4 import BeautifulSoup
from Fish import Fish

class FishScraper:
    def __init__(self, html):
        self.fishes = self._scrape(html)

    #scrapes fish according to the Northern Hemisphere schedule
    def _scrape(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        #"roundy sortable" is the unique class of the fish table
        table = soup.find('table', 'roundy sortable')
        fishes = self._scrapeTable(table)
        return fishes

    def _scrapeTable(self, table):
        rows = table.find_all('tr') #tr = HTML table row
        fishes = []

        #0th row contains label columns, not actual fish info
        for row in rows[1:]:
            fish = self._scrapeRow(row)
            fishes.append(fish)

        return fishes

    def _scrapeRow(self, fishRow):
        #td = HTML table column within a row
        rowColumns = fishRow.find_all('td')

        timeAvailability = self._parseAndConvertTimeAvailability(rowColumns[5].small.string)

        fish = Fish(rowColumns[0].a.string.strip().lower(), # name
            rowColumns[1].a['href'], #image cdn uri
            int(rowColumns[2].string.strip()), #price
            rowColumns[3].string.strip().lower(), #location
            self._convertShadowSize(rowColumns[4].string.strip()), #shadow size
            timeAvailability[0], #start time
            timeAvailability[1], #end time
            self._scrapeAndConvertMonthAvailability(rowColumns[6:])) #month availability

        return fish

    #convert time availability to MySql compatible Time format
    #assumes start/end times are at the 0th minute
    def _parseAndConvertTimeAvailability(self, timeAvailability):
        if self._isAllDay(timeAvailability):
            return '00:00:00', '00:00:00'

        parsedTimeAvailability = timeAvailability.strip().lower().split(' ')
        
        #start time is parsedTimeAvailability[0:1]
        startTime = self._convertTimeAvailability(parsedTimeAvailability[0:2])
        #end time is parsedTimeAvailability[3:4]
        endTime = self._convertTimeAvailability(parsedTimeAvailability[3:5])

        return startTime, endTime

    def _isAllDay(self, timeAvailability):
        if timeAvailability.strip().lower() == 'all day':
            return True
        return False

    def _convertTimeAvailability(self, timeAvailability):
        time = int(timeAvailability[0])
        if timeAvailability[1] == 'pm':
            time = (time + 12) % 24
        
        return str(time) + ':00:00'

    def _convertShadowSize(self, shadowSize):
        try:
            int(shadowSize)
            return int(shadowSize)
        except ValueError:
            return 7

    #returns a list of Booleans representing month availability in chronological order
    def _scrapeAndConvertMonthAvailability(self, monthAvailabilityColumns):
        monthAvailability = []

        for column in monthAvailabilityColumns:
            availability = False if column.string.strip() == '-' else True
            monthAvailability.append(availability)

        return monthAvailability

