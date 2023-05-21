from parsers import timestamp
from jinja2 import Environment, FileSystemLoader

def get_home_page(site_info, simTime):
    environment = Environment(loader=FileSystemLoader("data/templates/"))
    template = environment.get_template("homePage.html")
    #if no content header has been provided, the content header becomes the name of the file
    with open(f"_site/home.html", mode="w", encoding="utf-8") as message:
        message.write(template.render(
            #reverse the list order so newest entries are displayed first
            riders = reversed(site_info.items()),
            year = simTime["year"],
            day = simTime["day"],
            clock = timestamp(simTime)
            ))
        
def get_user_page(site_info, userID, userInfo):
    environment = Environment(loader=FileSystemLoader("data/templates/"))
    template = environment.get_template("userPage.html")
    with open(f"_site/users/{userID}.html", mode="w", encoding="utf-8") as message:
        message.write(template.render(
            #reverse the list order so newest entries are displayed first
            rider = site_info[f"{userID}"],
            ID = userID,
            loglist = userInfo[f"{userID}"]["log"]
            ))

def get_station_list(stations):
    environment = Environment(loader=FileSystemLoader("data/templates/"))
    template = environment.get_template("stations.html")
    stationsDictList = []
    for station in stations:
        slotsInUse = len(station.get_slots("full"))
        stationsDictList.append({"ID": station.ID, "naam": station.naam, "slotsInUse": slotsInUse})
    with open(f"_site/stations.html", mode="w", encoding="utf-8") as message:
        message.write(template.render(
            stations = stationsDictList
            ))
        
def get_station_info(station):
    environment = Environment(loader=FileSystemLoader("data/templates/"))
    template = environment.get_template("station.html")
    slotsInUse = len(station.get_slots("full"))
    with open(f"_site/stations/{station.ID}.html", mode="w", encoding="utf-8") as message:
        message.write(template.render(
            thisStation = station
            ))