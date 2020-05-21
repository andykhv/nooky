import mysql.connector

class FishSQLConnector:
    def __init__(self, user, database):
        self.connection = mysql.connector.connect(user=user, database=database)

    def populate(self, fishes):
        cursor = self.connection.cursor()

        fishTemplate = ("insert into fishes "
            "(name, imageURI, location, shadowSize, startTime, endTime, january, february, march, april, may, june, july, august, september, october, november, december) "
            "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        for fish in fishes:
            fishTuple = (fish.name, fish.imageURI, fish.location, fish.shadowSize, fish.startTime,
                fish.endTime, fish.monthAvailability[0], fish.monthAvailability[1], fish.monthAvailability[2], fish.monthAvailability[3], 
                fish.monthAvailability[4], fish.monthAvailability[5], fish.monthAvailability[6], fish.monthAvailability[7],
                fish.monthAvailability[8], fish.monthAvailability[9], fish.monthAvailability[10], fish.monthAvailability[11]) 

            cursor.execute(fishTemplate, fishTuple)

        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()
