import csv


# Package class to create package objects and override string
class Package:

    # Constructor for the package object
    def __init__(self, id, address, city, state, zip, deliveryDeadline, weight, notes, status, departureTime,
                 deliveryTime, truck):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = departureTime
        self.deliveryTime = deliveryTime
        self.truck = truck

    # Override for the string value of the package object, changes depending on the value of the deliveryTime component
    def __str__(self):
        if self.deliveryTime is None:
            return "%s | %s, %s, %s, %s | %s | %s | %s | %s | %s | %s | %s" % (
                "ID: " + str(self.id), "Address: " + self.address, self.city, self.state, self.zip,
                "Deadline: " + self.deliveryDeadline, "Weight: " + self.weight, "Notes: " + self.notes,
                "Status: " + self.status,
                "Departure Time: " + self.departureTime.strftime("%H:%M:%S"),
                "Delivery Time: NA", "Carried By: " + self.truck)
        else:
            return "%s | %s, %s, %s, %s | %s | %s | %s | %s | %s | %s | %s" % (
                "ID: " + str(self.id), "Address: " + self.address, self.city, self.state, self.zip,
                "Deadline: " + self.deliveryDeadline, "Weight: " + self.weight, "Notes: " + self.notes,
                "Status: " + self.status,
                "Departure Time: " + self.departureTime.strftime("%H:%M:%S"),
                "Delivery Time: " + self.deliveryTime.strftime("%H:%M:%S"), "Carried By: " + self.truck)

    # Method to adjust the status and deliveryTime of the package object to reflect the user inputted time.
    def checkTime(self, inputTime):
        if self.deliveryTime > inputTime:
            if self.departureTime <= inputTime:
                self.status = "En Route"
                self.deliveryTime = None
            if self.departureTime > inputTime:
                self.status = "At Hub"
                self.deliveryTime = None
        else:
            self.status = "Delivered"

# Loads the package data from the csv file and returns a hashtable populated with all the package data from the file
def loadPackageData(filename, hashtable):
    with open(filename) as packages:
        packageData = csv.reader(packages, delimiter=',')
        next(packageData)
        for package in packageData:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeliveryDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At Hub"
            pDepartureTime = None
            pDeliveryTime = None
            pTruck = None

            package = Package(pId, pAddress, pCity, pState, pZip, pDeliveryDeadline,
                              pWeight, pNotes, pStatus, pDepartureTime, pDeliveryTime, pTruck)

            hashtable.insert(pId, package)

        return hashtable
