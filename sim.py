import time
import random
import keyboard
from parsers import pickle_to_dict, dict_to_pickle, dict_to_json, json_to_dict
from infoFill import save_data, gen_new_sim
from runtime import *

def loop(speed_factor, saveFile=None, saveTo="sim.pkl"):
    if (saveFile is None):
        gen_new_sim()
        riders = {}
        walking = []
        bikesInUse = []
        almost_empty = []
        almost_full = []
        sim_seconds = 0
        sim_start = time.time()

    else:
        simfo = pickle_to_dict(saveFile)
        sim_start = time.time() - simfo["runningTime"]
        sim_seconds = simfo["sim_seconds"]
        riders = simfo["riders"]
        walking = simfo["walking"]
        bikesInUse = simfo["bikesInUse"]
        almost_empty = simfo["almost_empty"]
        almost_full = simfo["almost_full"]
    
    data = pickle_to_dict("data.pkl")
    gebruikers = data["gebruikers"]
    fietsen = data["fietsen"]
    stations = data["stations"]
    transporteurs = data["transporteurs"]

    stop = False

    while (stop == False):
        sim_seconds += 1
        real_seconds = int(time.time() - sim_start)
        start_time = time.time()  # Start time of the iteration

        # Perform the random action
        print(f"{sim_seconds} ({real_seconds} real time seconds)")


        elapsed_time = time.time() - start_time  # Elapsed time of the iteration
        remaining_time = (60.0/speed_factor) - elapsed_time  # Remaining time until one second

        if remaining_time > 0:
            time.sleep(remaining_time)

        if keyboard.is_pressed('g'):
            break
    #save data for next time
    sim_save = {"runningTime": time.time() - sim_start, "sim_seconds": sim_seconds, "riders": riders, "walking": walking, "bikesInUse": bikesInUse, "almost_empty": almost_empty, "almost_full": almost_full}
    dict_to_pickle(saveTo, sim_save)
    save_data()
    
loop(600, "sim.pkl")