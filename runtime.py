from infoFill import gen_new_sim

def initialize_new(aantalGebruikers = 55000, aantalFietsen = 4200, aantalTransporteurs=5):
    gen_new_sim(aantalGebruikers, aantalFietsen, aantalTransporteurs)

initialize_new()

def user_get_bike(user, station, forTime):
    #user takes bike
    #'target time: user, bike' gets added to 'riders' dictionary
    #when elapsed time == target time -> user returns bike
    return None
    
def user_return_bike(user, station):
    #search stations
    #if station not full -> store bike
    #user gets re-added to 'walking' dictionary
    return None

def mover_take_bikes(mover, station, forTime, bikeAmount):
    #dictionary stations that are overful (80% full or more)
    #mover takes specified amount of bikes from station
    #target time gets set
    #'target time: {user: user, bikes: bikelist}' added to 'riders' dictionary using for-loop riders[target-time]
    return None

def mover_place_bikes(mover, station, bikeAmount):
    return None