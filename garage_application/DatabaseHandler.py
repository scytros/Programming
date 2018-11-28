import jsonpickle
import random

jsonFilePath = "Database.json"      # Filepath for the json database
with open(jsonFilePath, "w") as startFile:
    startFile.write("")     # Empties the database and makes it ready for use

availableIds = []       # All parkingid's that can be used
availableIds.extend(range(0, 100))
takenIds = []       # All the parkingid's that are being used


def to_database(dataHolder):
    """"Creates a json representation of the data and saves it to the database"""

    parkingId = generate_id()
    dataHolder.add_parkingId(parkingId)

    jsonString = jsonpickle.encode(dataHolder)

    with open(jsonFilePath, 'ab+') as jsonFile:
        if jsonFile.tell() == 0:
            jsonFile.write(jsonpickle.dumps([jsonString]).encode())
        else:
            jsonFile.seek(0, 2)     # Go to the end of file
            jsonFile.seek(-1, 2)
            jsonFile.truncate()     # Remove the last character, open the array
            jsonFile.write(' , '.encode())      # Write the separator
            jsonFile.write(jsonpickle.dumps(jsonString).encode())       # Dump the dictionary
            jsonFile.write(']'.encode())

    return parkingId


def from_database(id, leaveGarage):
    """"Reads a jsonstring from the database"""

    with open(jsonFilePath, "r") as jsonFile:
        dictList = jsonpickle.loads(jsonFile.read())
        for dict in dictList:
            dataHolder = jsonpickle.decode(dict)
            if dataHolder.ParkingId == id:
                if leaveGarage:
                    takenIds.remove(id)
                    availableIds.append(id)
                    dictList.remove(dict)
                    with open(jsonFilePath, "w") as changedJsonFile:
                        if len(dictList) > 0:
                            changedJsonFile.write(jsonpickle.dumps(dictList))
                        else:
                            changedJsonFile.write("")
                return dataHolder


def generate_id():
    """"Generates an ID that has not been used yet"""

    generatedId = random.choice(availableIds)       # Generates an IndexError when all ID's have been used. but the available ID's should be enough for proof of concept.
    while generatedId not in takenIds:
        takenIds.append(generatedId)
        availableIds.remove(generatedId)

    return generatedId