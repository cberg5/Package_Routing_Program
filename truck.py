
# Truck class to create truck objects and override the string value of a truck object
class Truck:

    # Constructor for a truck object
    def __init__(self, name, location, mileage, packages, time):
        self.name = name
        self.location = location
        self.mileage = mileage
        self.packages = packages
        self.time = time
