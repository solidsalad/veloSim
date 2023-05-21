import random
from parsers import json_to_dict, vals


class Station():
    ID = 0
    def __init__(self, district, aantalPlaatsen, naam):
        self.ID = "st"+str(Station.ID)
        Station.ID += 1
        self.district = district
        self.naam = naam
        self.slots = []
        for i in range(aantalPlaatsen):
            self.slots.append(Slot())

    def __str__(self):
        string = f"station - ID {self.ID}: '{self.naam}': {len(self.slots)} slots ({len(self.slots) - len(self.get_slots('empty'))} occupied):"
        for slot in self.slots:
            if (slot.bike == None):
                info = "empty"
            else:
                info = f"bike {slot.bike.ID}"
            string += f"\n\t- slot {slot.ID}: {info}"
        return string


    def get_slots(self, state):    
        slots = []
        if (state == "empty"):
            for slot in self.slots:
                if (slot.bike == None):
                    slots.append(slot)
        elif (state == "full"):
            for slot in self.slots:
                if (slot.bike != None):
                    slots.append(slot)
        else:
            print(f"ERROR: slot state {state} unknown")
        return slots


class Fiets():
    ID = 0
    def __init__(self):
        self.ID = "f"+str(Fiets.ID)
        Fiets.ID += 1
        self.inUse = False
    
    def __str__(self):
        if (self.inUse == False):
            return f"fiets - ID {self.ID}: niet in gebruik"
        else:
            return f"fiets - ID {self.ID}: momenteel in gebruik"

class Slot():
    ID = 0
    def __init__(self):
        self.ID = "s"+str(Slot.ID)
        Slot.ID += 1
        self.bike = None
    
    def store_bike(self, bike):
        bike.inUse = False
        self.bike = bike
    
    def get_bike(self):
        self.bike.inUse = True
        bike = self.bike
        self.bike = None
        return bike


class Gebruiker():
    names = json_to_dict("names.json")
    ID = 0 
    def __init__(self):
        self.ID = "u"+str(Gebruiker.ID)
        Gebruiker.ID += 1
        self.userType="gebruiker"
        self.naam = Gebruiker.generate_name()
        self.bikes = [None]
        self.maxBikes = 1
        self.latestLog = ""

    def __str__(self):
        if (len(vals(self.bikes)) == 0):
            user_str = f"{self.userType} - ID {self.ID}: '{self.naam}' geen fiets"
        else:
            user_str = f"{self.userType} - ID {self.ID}: '{self.naam}' gebruikt fiets ID:"
            for bike in vals(self.bikes):
                user_str = user_str + f"{bike.ID}, "
            user_str = user_str[:-2]
        return user_str
    
    def generate_name():
        firstName = Gebruiker.names["first names"][random.randint(0,(len(Gebruiker.names["first names"])-1))]
        lastName = Gebruiker.names["last names"][random.randint(0,(len(Gebruiker.names["last names"])-1))]
        return f"{firstName} {lastName}"

    def user_store_bike(self, station, amount=1):
        emptySlots = station.get_slots("empty")
        if (len(vals(self.bikes)) == 0):   
            print(f"ERROR: {self.userType} {self.ID} cannot store a bike because he doesn't have one")
        else:
            i = 0
            for bike in self.bikes:
                if (bike is not None) and (i < amount):
                    if (len(emptySlots) == 0):
                        print(f"ERROR: {self.userType} {self.ID} cannot store bike {bike.ID}: station full")
                    else:
                        slot = emptySlots[random.randint(0, len(emptySlots)-1)]
                        self.latestLog = f"stored {bike.ID} into slot {slot.ID} at station {station.ID}"
                        print(f"log: user {self.ID} stored {bike.ID} into slot {slot.ID} at station {station.ID}")
                        slot.store_bike(bike)
                        bike = None
                i += 1

    def user_get_bike(self, station, amount=1):
        if (amount <= self.maxBikes):
            fullSlots = station.get_slots("full")
            if (len(fullSlots) == 0):
                print(f"ERROR: {self.userType} {self.ID} cannot get a bike: station empty")
            i = 0
            for bike in self.bikes:
                if (bike is None) and (i < amount):
                    fullSlots = station.get_slots("full")
                    if (len(vals(self.bikes)) >= self.maxBikes):
                        print(f"ERROR: {self.userType} {self.ID} cannot get a bike: user already has max amount of bikes")
                    else:
                        slot = fullSlots[random.randint(0, len(fullSlots)-1)]
                        self.latestLog = f"taken {slot.bike.ID} from slot {slot.ID} at station {station.ID}"
                        self.bikes[i] = slot.get_bike()
                i += 1
        else:
            print(f"ERROR: {self.userType} cannot take more than {self.maxBikes} bike(s)")

class Transporteur(Gebruiker):
    ID = 0
    def __init__(self, maxBikes):
        super().__init__()
        self.ID = "tr"+str(Transporteur.ID)
        Transporteur.ID += 1
        self.userType = "transporteur"
        self.maxBikes = maxBikes
        self.bikes = []
        for i in range(self.maxBikes):
            self.bikes.append(None)

class Rit():
    ID = 0
    def __init__(self, startTime, endTime, user, station, amount=1):
        self.ID = Rit.ID
        Rit.ID += 1
        self.startTime = startTime
        self.endTime = endTime
        self.user = user
        self.user.user_get_bike(station, amount)
        self.bikes = vals(self.user.bikes)
        print(f"ride {self.ID} until {self.endTime} ({self.endTime - self.startTime} minutes) (user {self.user.ID} ({self.user.naam}), bike(s) {[bike.ID for bike in self.bikes]})")

    def drop_bike(self, station, amount=1):
        self.user.user_store_bike(station, amount)
        self.bikes = self.user.bikes
            
    
