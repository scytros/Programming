import tkinter as tk
import tkinter.filedialog
import requests
import datetime
import Licencing
import Encryption
import DatabaseHandler
import DataHolder

root = tk.Tk()  # Tkinter root
root.attributes("-topmost", True)
root.withdraw()  # Withdraw the TKinter window

isRunning = True


def allow_only_bool_input(prompt):
    """"Allow only true or false input"""

    while True:
        try:
            return {"ja": True, "nee": False}[input(prompt).lower()]
        except KeyError:
            print("\nAlleen 'ja' of 'nee' alstublieft.")


def vehicle_check_flow(fuel, modelName, brand, buildDate):
    """"Check if the vehicle is allowed, and act upon the decision"""

    if (fuel == "Diesel") and int(buildDate) < 2001:
        print("\nUw", brand, modelName, "is een auto die op diesel rijdt en voor 2001 is gebouwd. \nDeze auto mag helaas de parkeergarage niet in.")
    else:
        print("\nUw {0} {1} uit {2} mag de parkeergarage in. \nWelkom!".format(brand, modelName, buildDate))

        timeStampAsBytes = str(datetime.datetime.now()).encode()
        plateDataAsBytes = plateData.encode()

        encryptedPlate = Encryption.encrypt(plateDataAsBytes)
        encryptedTimeStamp = Encryption.encrypt(timeStampAsBytes)

        dataHolder = DataHolder.DataHolder(encryptedPlate, encryptedTimeStamp)
        parkingId = DatabaseHandler.to_database(dataHolder)

        leaveGarage = allow_only_bool_input("\nWilt u uitrijden? 'ja' of 'nee'.")
        jsonItem = DatabaseHandler.from_database(parkingId, leaveGarage)

        print("\nUw parkeerID is: {0} Uw kenteken: {1} Uw inrijtijd: {2}".format(jsonItem.ParkingId, Encryption.decrypt(jsonItem.EncryptedPlate), (Encryption.decrypt(jsonItem.EncryptedTime))))
        if leaveGarage:
            print("U bent uit de database verwijderd. Tot ziens!")


while isRunning:
    plateFileName = tk.filedialog.askopenfilename()
    while plateFileName == "":
        plateFileName = tk.filedialog.askopenfilename()

    file = {'image': ('image', open(plateFileName, 'rb'))}
    # testFilePath = b'D:\Users\Stan\PycharmProjects\Project_Prog\Images\BMW.jpg'  # Test file path
    # file = {'image': ('image', open(testFilePath, 'rb'))}       # Test file

    print("\nData aan het ophalen...")

    responseAlpr = requests.post(Licencing.alprUrl, files=file)
    data = responseAlpr.json()

    plateData = Licencing.get_license(data)  # The licence plate data
    vehicleInfo = Licencing.send_plate(plateData)  # The info about the vehicle

    fuel = ""
    modelName = ""
    brand = ""
    buildDate = ""

    try:
        fuel = vehicleInfo["hoofdbrandstof"]
        modelName = vehicleInfo["handelsbenaming"]
        brand = vehicleInfo["merk"]
        buildDate = int(vehicleInfo["datumeerstetoelating"].split("-")[0])
        vehicle_check_flow(fuel, modelName, brand, buildDate)
    except KeyError:
        print("\nOver deze auto is helaas geen informatie te vinden.")
    except TypeError:
        print("\nOver deze auto is helaas geen informatie te vinden.")
        continue

    tryAgain = allow_only_bool_input("\nWilt u nog een auto testen? 'ja' of 'nee'.")

    if not tryAgain:
        break

print("\nOké, bedankt voor het gebruik maken van deze applicatie!")