import random
from parsers import json_to_dict, dict_to_pickle, pickle_to_dict
from classes import *
import os

def delete_folder_content(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_folder_content(file_path)
            os.rmdir(file_path)


def make_stations():
    Station.ID = 0
    Slot.ID = 0
    stationFile = json_to_dict("velo.json")
    stations = []
    for station in stationFile["features"]:
        info = station["properties"]
        newStation = Station(district=info["District"], aantalPlaatsen=info["Aantal_plaatsen"], naam=info["Naam"])
        stations.append(newStation)
    return stations

def make_gebruikers(aantalGebruikers):
    Gebruiker.ID = 0
    gebruikers = []
    for newUser in range(aantalGebruikers):
        newUser = Gebruiker()
        gebruikers.append(newUser)
    return gebruikers

def make_transporteurs(aantalTransporteurs):
    transporteurs = []
    for newTransporter in range(aantalTransporteurs):
        newTransporter = Transporteur(random.randint(10,31))
        transporteurs.append(newTransporter)
    return transporteurs

def make_fietsen(aantalFietsen):
    max_value = sum(station["properties"]["Aantal_plaatsen"] for station in json_to_dict("velo.json")["features"])
    if aantalFietsen > max_value:
        print(f"aantal fietsen kan niet meer zijn aantal beschikbare slots ({max_value} slots)")
        aantalFietsen = max_value
    Fiets.ID = 0
    fietsen = []
    for newFiets in range(aantalFietsen):
        newFiets = Fiets()
        fietsen.append(newFiets)
    return fietsen

def fill_stations(stations, fietsen):
    for fiets in fietsen:
        slotted = False
        while (slotted == False):
            station = stations[random.randint(0, len(stations)-1)]
            avSlots = station.get_slots("empty")
            if (len(avSlots) > 0):
                slot = avSlots[random.randint(0, len(avSlots)-1)]
                slot.bike = fiets
                slotted = True

def gen_new_sim(aantalGebruikers = 55000, aantalFietsen = 4200, aantalTransporteurs=5):
        transporteurs = make_transporteurs(aantalTransporteurs)
        gebruikers = make_gebruikers(aantalGebruikers)
        stations = make_stations()
        fietsen = make_fietsen(aantalFietsen)
        fill_stations(stations, fietsen)
        save_data(stations, gebruikers, fietsen, transporteurs)

def save_data(stations=pickle_to_dict("data.pkl")["stations"], gebruikers=pickle_to_dict("data.pkl")["gebruikers"], fietsen=pickle_to_dict("data.pkl")["fietsen"], transporteurs=pickle_to_dict("data.pkl")["transporteurs"]):
    info = {"stations": stations, "gebruikers": gebruikers, "fietsen": fietsen, "transporteurs": transporteurs}
    dict_to_pickle("data.pkl", info)





