import time
import random
import keyboard
from parsers import pickle_to_dict, dict_to_pickle, dict_to_json, json_to_dict, vals
from infoFill import save_data, gen_new_sim
from getRandom import getRandom
from classes import Rit

def loop(speed_factor, saveFile=None, saveTo="sim.pkl"):
    if (saveFile is None):
        gen_new_sim()
        riders = {}
        currently_transp = {}
        available_transp = []
        walking = []
        bikesInUse = []
        almost_empty = []
        almost_full = []
        sim_minutes = 0
        sim_start = time.time()

    else:
        simfo = pickle_to_dict(saveFile)
        sim_start = time.time() - simfo["runningTime"]
        sim_minutes = simfo["sim_seconds"]
        riders = simfo["riders"]
        walking = simfo["walking"]
        bikesInUse = simfo["bikesInUse"]
        almost_empty = simfo["almost_empty"]
        almost_full = simfo["almost_full"]
        currently_transp = simfo["currently_transp"]
        available_transp = simfo["available_transp"]
    
    data = pickle_to_dict("data.pkl")
    gebruikers = data["gebruikers"]
    fietsen = data["fietsen"]
    stations = data["stations"]
    transporteurs = data["transporteurs"]

    if (saveFile is None):
        available_transp = [transporteur for transporteur in transporteurs if (len(vals(transporteur.bikes)) < transporteur.maxBikes)]
        walking = [gebruiker for gebruiker in gebruikers if (len(vals(gebruiker.bikes)) < gebruiker.maxBikes)]

    stop = False

    while (stop == False):
        sim_minutes += 1
        real_seconds = int(time.time() - sim_start)
        start_time = time.time()  # Start time of the iteration

        #getting bike
        if (random.randint(1,3) == 1):
            for i in range(random.randint(1,10)):
                stat = getRandom(stations)
                if (len(stat.get_slots("empty")) < len(stat.slots)):
                    endTime = sim_minutes + random.randint(20,120)
                    if str(endTime) not in riders.keys():
                        riders[f"{endTime}"] = []
                    user = getRandom(walking)
                    riders[f"{endTime}"].append(Rit(sim_minutes, endTime, user, getRandom(stations)))
                    walking.remove(user)

        #returning bike
        if (str(sim_minutes) in riders.keys()):
                for rit in riders[f"{sim_minutes}"]:
                    stat = getRandom(stations)
                    if (len(stat.get_slots("full")) < len(stat.slots)):
                        #end trip
                        rit.drop_bike(stat)
                        walking.append(rit.user)
                    else:
                        #extend time and go to different station because current station is full
                        rit.endTime += random.randint(5,20)
                        if str(rit.endTime) not in riders.keys():
                            riders[f"{rit.endTime}"] = []
                        riders[f"{rit.endTime}"].append(rit)
                del riders[f"{sim_minutes}"]
                

        #checking which stations are almost full
        almost_full = [station for station in stations if (len(station.get_slots("full")) >= 0.8*len(station.slots))]
        
        #checking which stations are almost empty
        almost_empty = [station for station in stations if (len(station.get_slots("empty")) >= 0.8*len(station.slots))]

        #loading up bikes from (almost) full stations
        if (random.randint(1,4) == 1) and (len(available_transp) >= 2):
            endTime = sim_minutes + random.randint(5,30)
            if str(endTime) not in currently_transp.keys():
                currently_transp[f"{endTime}"] = []
            user = getRandom(available_transp)
            full_stat = getRandom(almost_full)
            amount = random.randint(int(0.3*len(full_stat.get_slots("full"))),int(0.6*len(full_stat.get_slots("full"))))
            if (amount > user.maxBikes):
                amount = user.maxBikes
            currently_transp[f"{endTime}"].append(Rit(sim_minutes, endTime, user, full_stat, amount))
            available_transp.remove(user)

        #dropping bikes at (almost) empty stations
        if (str(sim_minutes) in currently_transp.keys()):
            for rit in currently_transp[f"{sim_minutes}"]:
                if (len(almost_empty) > 0):
                    stat = getRandom(almost_empty)
                    amount = (0.6* len(stat.slots)) - len(stat.get_slots("full"))
                    if (amount >= len(vals(rit.bikes))):
                        rit.drop_bike(stat, len(vals(rit.bikes)))
                        available_transp.append(rit.user)
                    else:
                        #drop needed bikes, extend time, and go to different station because current station does not need any more bikes
                        rit.drop_bike(stat, len(vals(rit.bikes)))
                        rit.endTime += random.randint(5,30)
                        if str(rit.endTime) not in currently_transp.keys():
                            currently_transp[f"{rit.endTime}"] = []
                        currently_transp[f"{rit.endTime}"].append(rit)
                else:
                    rit.endTime += random.randint(5,30)
                    if str(rit.endTime) not in currently_transp.keys():
                        currently_transp[f"{rit.endTime}"] = []
                    currently_transp[f"{rit.endTime}"].append(rit)                    
            del currently_transp[f"{sim_minutes}"]
        
        print(f"{sim_minutes} ({real_seconds} real time seconds)")
        #stop complete loop

        elapsed_time = time.time() - start_time  # Elapsed time of the iteration
        remaining_time = (60.0/speed_factor) - elapsed_time  # Remaining time until one second

        if remaining_time > 0:
            time.sleep(remaining_time)

        if keyboard.is_pressed('g'):
            stop = True
    #save data for next time
    sim_save = {"runningTime": time.time() - sim_start, "sim_seconds": sim_minutes, "riders": riders, "walking": walking, "bikesInUse": bikesInUse, "almost_empty": almost_empty, "almost_full": almost_full, "currently_transp": currently_transp, "available_transp": available_transp}
    dict_to_pickle(saveTo, sim_save)
    save_data()
    
loop(600, 'sim.pkl')