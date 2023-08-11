# Author: Cody Bergin, Student ID: 010822887

from datetime import datetime, timedelta
import csv
from hashTable import ChainingHashTable
from package import loadPackageData, Package
from truck import Truck

# Create hash table and load package data into hash table from package csv file
packageHash = ChainingHashTable()
packageHash = loadPackageData('csv/packageFile.csv', packageHash)

# Load distance data into a list from distance csv file
distanceData = list(csv.reader(open('csv/distanceTable.csv', encoding='utf-8-sig')))

# Load address data into a list from address csv file
addressData = list(csv.reader(open('csv/addressTable.csv', encoding='utf-8-sig')))


# Finds the distance in miles between two addresses by accessing the two-dimensional array of distance data
def distanceBetween(address1, address2):
    return distanceData[addressData.index([address2])][addressData.index([address1])]


# Finds the closest address from the trucks packages to the current address
def closestDistance(currentAddress, truckPackages):
    # Fill list of all distances between current address and all truck packages
    distances = []
    for package in truckPackages:
        distances.append(float(distanceBetween(currentAddress, package.address)))

    # Find and return the address for the package that matches the minimum from the distance list
    for package in truckPackages:
        if min(distances) == float(distanceBetween(currentAddress, package.address)):
            return package.address


def deliverPackages(truck):
    truckPackages = []
    # Fill list of all packages on the truck.
    # Update all packages to being "En Route" and departure time to the truck's current time
    for packageId in truck.packages:
        package = packageHash.search(packageId)
        package.status = "En Route"
        package.departureTime = truck.time
        package.truck = truck.name
        truckPackages.append(package)

    # Loop while truckPackages list still has elements
    while truckPackages:

        # Loop through all addresses on the trucks route.
        for package in truckPackages:

            # Use closestDistance method to find the address on the route that is closest to the trucks current location
            if closestDistance(truck.location, truckPackages) == package.address:
                # Find how long in minutes and seconds that the truck will take to travel to the closest address and
                # add that time to the trucks time
                minutes = int(60 * (float(distanceBetween(truck.location, package.address)) / 18))
                seconds = int(60 * (60 * (float(distanceBetween(truck.location, package.address)) / 18) % 1))
                truck.time += timedelta(minutes=minutes, seconds=seconds)

                # Update truck mileage with the distance to travel to the closest address
                truck.mileage += float(distanceBetween(truck.location, package.address))

                # Update the truck's current location with the closest address
                truck.location = package.address

                # Update package status to "delivered" and delivery time to the truck's time
                package.status = "Delivered"
                package.deliveryTime = truck.time
                # Remove package from the list since it's been delivered
                truckPackages.remove(package)


# Create truck objects. Set starting address to "hub" address. Set initial mileage to 0.0.
# Manually load packages. Set time to truck departure time.
# 1st truck set to depart at 8.
truck1 = Truck("Truck 1", "4001 South 700 East", 0.0, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
               datetime(datetime.now().year, datetime.now().month, datetime.now().day, 8, 0, 0))

# 2nd truck set to depart at 9:05, to accommodate packages that arrived at 9:05.
truck2 = Truck("Truck 2", "4001 South 700 East", 0.0, [3, 6, 18, 25, 28, 32, 33, 35, 36, 38, 39],
               datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 5, 0))

# 3rd truck set to depart at 10:20 to accommodate package 9 that has the address change at 10:20
truck3 = Truck("Truck 3", "4001 South 700 East", 0.0, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27],
               datetime(datetime.now().year, datetime.now().month, datetime.now().day, 10, 20, 0))

# Deliver packages from the three trucks
deliverPackages(truck1)
deliverPackages(truck2)
deliverPackages(truck3)


# Main class to implement command line user interface
class Main:
    # Show program initializing and how many miles the trucks traveled
    print("WGUPS Routing Program")
    print()
    print("Total miles traveled by all trucks is {}".format(truck1.mileage + truck2.mileage + truck3.mileage))
    print()

    # Ask user for a time as input to then show the status of all the packages at that time
    # Try and except used to verify user inout is of the correct format. Exits program if incorrect
    try:
        inputTime = input("View package status at specific time. Enter time in HH:MM:SS\n")
        hour, min, sec = [int(i) for i in inputTime.split(":")]
        time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hour, min, sec)
        print("Package Status at: " + time.strftime("%H:%M:%S"))
        for i in range(1, 41):
            package = packageHash.search(i)
            package.checkTime(time)
            print(str(package))

    except ValueError:
        print("Invalid Input, Try again")
