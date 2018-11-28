import json

class DataHolder:
    """"An object to hold encrypted data for the jsonstring"""

    def __init__(self, encryptedPlate, encryptedTime):
        self.ParkingId = 0
        self.EncryptedPlate = encryptedPlate
        self.EncryptedTime = encryptedTime

    def add_parkingId(self, parkingId):
        """"Adds a parking id to this instance"""

        self.ParkingId = parkingId

    def serialize_to_json(self):
        """"Serializes this object to valid json"""

        return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True, indent=4)

    def print_data(self):
        """"Prints the instance variables of this class"""

        print("Encrypted LicencePlate: {0}".format(self.EncryptedPlate))
        print("Encrypted Time Of Arrival: {0}".format(self.EncryptedTime))
        print("Parking ID: {0}".format(self.ParkingId))
