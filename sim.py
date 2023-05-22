import time
import random
import keyboard
from parsers import pickle_to_dict, dict_to_pickle, dict_to_json, json_to_dict, vals, tick_to_time, timestamp
from infoFill import save_data, gen_new_sim, getRandom
from website import get_home_page, get_user_page, get_station_list, get_station_info
from infoFill import delete_folder_content
from classes import Rit

def loop(speed_factor, saveFile=None, saveTo="sim.pkl"):

    save = True

    if (saveFile is None):
        gen_new_sim()
        delete_folder_content("_site/users")
        riders = {}
        currently_transp = {}
        available_transp = []
        walking = []
        bikesInUse = []
        almost_empty = []
        almost_full = []
        site_info = {}
        userInfo = {}
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
        site_info = json_to_dict("site_info.json")
        userInfo = json_to_dict("userInfo.json")
    
    data = pickle_to_dict("data.pkl")
    gebruikers = data["gebruikers"]
    fietsen = data["fietsen"]
    stations = data["stations"]
    transporteurs = data["transporteurs"]

    if (saveFile is None):
        available_transp = [transporteur for transporteur in transporteurs if (len(vals(transporteur.bikes)) < transporteur.maxBikes)]
        walking = [gebruiker for gebruiker in gebruikers if (len(vals(gebruiker.bikes)) < gebruiker.maxBikes)]
        for gebruiker in gebruikers:
            userInfo[f"{gebruiker.ID}"] = {}
            userInfo[f"{gebruiker.ID}"]["name"] = f"{gebruiker.naam} ({gebruiker.ID})"
            userInfo[f"{gebruiker.ID}"]["log"] = []
        for transporteur in transporteurs:
            userInfo[f"{transporteur.ID}"] = {}
            userInfo[f"{transporteur.ID}"]["name"] = f"{transporteur.naam} ({transporteur.ID})"
            userInfo[f"{transporteur.ID}"]["log"] = []

    prev_sec = 0
    stop = False

    get_station_list(stations)

    while (stop == False):
        sim_minutes += 1
        real_seconds = int(time.time() - sim_start)
        start_time = time.time()  # Start time of the iteration
        simTime = tick_to_time(sim_minutes)
        chosenStation = None


        #getting bike
        if (random.randint(1,3) == 1):
            for i in range(random.randint(1,10)):
                stat = getRandom(stations)
                if (len(stat.get_slots("empty")) < len(stat.slots)):
                    endTime = sim_minutes + random.randint(20,120)
                    if str(endTime) not in riders.keys():
                        riders[f"{endTime}"] = []
                    user = getRandom(walking)
                    thisRit = Rit(sim_minutes, endTime, user, stat)
                    #log taking bike + timestamp
                    userInfo[f"{user.ID}"]["log"].append({"timeStamp": timestamp(simTime), "message": user.latestLog})
                    riders[f"{endTime}"].append(thisRit)
                    #log to site info
                    if (str(user.ID) in site_info.keys()):
                        del site_info[f"{user.ID}"]
                    userString = str(user)
                    userBikes = [bike.ID for bike in user.bikes]
                    site_info[f"{user.ID}"] = {"string": userString, "bikes": userBikes, "progress": 0, "timeTag": f"{timestamp(simTime)}", "start": sim_minutes, "end": endTime}
                    get_user_page(site_info, user.ID, userInfo)
                    walking.remove(user)

        #manual actions
        if keyboard.is_pressed('ctrl'):
            print("\npause -- manuele interventie\n")
            answer = input("velo menu:\n1. Fiets ontlenen\n2. fiets terugbrengen\n3. verder gaan met simulatie\n\nmaak je keuze: ")
            #fiets ontlenen
            if (answer == "1"):
                #user kiezen
                bikeTaker = None
                uOk = False
                while (uOk == False):
                    userChoice = input("\nkies gebruiker ID: u")
                    for walker in walking:
                        if (walker.ID == f"u{userChoice}"):
                            bikeTaker = walker
                            uOk = True
                    if (bikeTaker == None):
                        print(f'\nsorry, gebruiker u{userChoice} bestaat niet of heeft momenteel al een fiets, gelieve een andere gebruiker te kiezen:')
                #station kiezen
                chosenStation = None
                sOk = False
                while (sOk == False):
                    statChoice = input("\nkies station ID: st")
                    for temp_station in stations:
                        if (temp_station.ID == f"st{statChoice}"):
                            chosenStation = temp_station
                            if (len(chosenStation.get_slots("empty")) < len(stat.slots)):
                                sOk = True
                            else:
                                print(f'\n\n{len(chosenStation.get_slots("empty"))} < {len(stat.slots)}')
                                print("station is momenteel leeg, gelieve een ander station te kiezen:")
                    if (chosenStation == None):
                        print(f'\nsorry, station st{statChoice} bestaat niet , gelieve een ander station te kiezen:')                
                #fiets nemen
                endTime = sim_minutes + random.randint(20,120)
                if str(endTime) not in riders.keys():
                    riders[f"{endTime}"] = []
                thisRit = Rit(sim_minutes, endTime, bikeTaker, chosenStation)
                #log taking bike + timestamp
                userInfo[f"{bikeTaker.ID}"]["log"].append({"timeStamp": timestamp(simTime), "message": bikeTaker.latestLog})
                riders[f"{endTime}"].append(thisRit)
                #log to site info
                if (str(bikeTaker.ID) in site_info.keys()):
                    del site_info[f"{bikeTaker.ID}"]
                userString = str(bikeTaker)
                userBikes = [bike.ID for bike in bikeTaker.bikes]
                site_info[f"{bikeTaker.ID}"] = {"string": userString, "bikes": userBikes, "progress": 0, "timeTag": f"{timestamp(simTime)}", "start": sim_minutes, "end": endTime}
                get_user_page(site_info, bikeTaker.ID, userInfo)
                walking.remove(bikeTaker)                
            #fiets terugbrengen
            elif (answer == "2"):
                #user kiezen
                ride = None
                uOk = False
                while (uOk == False):
                    userChoice = input("\nkies fietser ID: u")
                    for this_timestamp in riders.values():
                        for this_rit in this_timestamp:    
                            if (this_rit.user.ID == f"u{userChoice}"):
                                this_ride = this_rit
                                uOk = True
                    if (this_ride == None):
                        print(f'\nsorry, gebruiker u{userChoice} bestaat niet of heeft geen fiets, gelieve een andere fietser te kiezen:')
                #station kiezen
                chosenStation = None
                sOk = False
                while (sOk == False):
                    statChoice = input("\nkies station ID: st")
                    for temp_station in stations:
                        if (temp_station.ID == f"st{statChoice}"):
                            chosenStation = temp_station
                            if (len(chosenStation.get_slots("full")) < len(stat.slots)):
                                sOk = True
                            else:
                                print("station is momenteel vol, gelieve een ander station te kiezen:")
                    if (chosenStation == None):
                        print(f'\nsorry, station st{statChoice} bestaat niet , gelieve een ander station te kiezen:')

                #setting end time to current tick
                if str(sim_minutes) not in riders.keys():
                    riders[f"{sim_minutes}"] = []
                riders[f"{sim_minutes}"].append(rit)
                #updating ride length
                site_info[f"{this_ride.user.ID}"]["end"] = sim_minutes
                
                #deleting it from previous endTime
                if (len(riders[f"{this_ride.endTime}"]) > 1):
                    riders[f"{this_ride.endTime}"].remove(rit)
                else:
                    del riders[f"{this_ride.endTime}"]
            elif (answer == "3"):
                continue
            else:
                print("onbekend commando -> simulatie gaat verder")

        #returning bike
        if (str(sim_minutes) in riders.keys()):
                for rit in riders[f"{sim_minutes}"]:
                    if (chosenStation == None):
                        stat = getRandom(stations)
                    else:
                        stat = chosenStation
                    if (len(stat.get_slots("full")) < len(stat.slots)):
                        #setting progress bars to 100% because ride is done
                        site_info[f"{rit.user.ID}"]["progress"] = 100
                        #end trip
                        rit.drop_bike(stat)
                        walking.append(rit.user)
                        #update user string (geen fiets)
                        site_info[f"{rit.user.ID}"]["string"] = str(rit.user)
                        #log return of bike
                        userInfo[f"{rit.user.ID}"]["log"].append({"timeStamp": timestamp(simTime), "message": rit.user.latestLog})
                        get_user_page(site_info, rit.user.ID, userInfo)
                    else:
                        #extend time and go to different station because current station is full
                        rit.endTime += random.randint(5,20)
                        if str(rit.endTime) not in riders.keys():
                            riders[f"{rit.endTime}"] = []
                        riders[f"{rit.endTime}"].append(rit)
                        site_info[f"{rit.user.ID}"]["end"] = rit.endTime
                        userInfo[f"{rit.user.ID}"]["log"].append({"timeStamp": timestamp(simTime), "message": f"station {stat.ID} full: extending rit to {rit.endTime - rit.startTime} minutes"})
                        get_user_page(site_info, rit.user.ID, userInfo)
                del riders[f"{sim_minutes}"]
        
        #updating progress for all riders
        for moment in riders.values():
            for rit in moment:
                start = site_info[f"{rit.user.ID}"]["start"]
                end = site_info[f"{rit.user.ID}"]["end"]
                site_info[f"{rit.user.ID}"]["progress"] = int(((sim_minutes - start)/(end - start))*100)

        #checking which stations are almost full
        almost_full = [station for station in stations if (len(station.get_slots("full")) >= 0.8*len(station.slots))]
        
        if keyboard.is_pressed('g'):
            stop = True

        #checking which stations are almost empty
        almost_empty = [station for station in stations if (len(station.get_slots("empty")) >= 0.8*len(station.slots))]

        #loading up bikes from (almost) full stations
        if (random.randint(1,4) == 1) and (len(available_transp) >= 2) and (len(almost_full) > 0):
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
        
        if keyboard.is_pressed('g'):
            stop = True

        #update site info every real second
        if (prev_sec != real_seconds) or (prev_sec == 0):
            get_home_page(site_info, simTime)
            for moment in riders.values():
                for rit in moment:
                    #updating rider progress bar
                    get_user_page(site_info, rit.user.ID, userInfo)
            #updating station info per station
            for station in stations:
                get_station_info(station)


        #stop complete loop

        prev_sec = real_seconds

        elapsed_time = time.time() - start_time  # Elapsed time of the iteration
        remaining_time = (60.0/speed_factor) - elapsed_time  # Remaining time until one second

        if remaining_time > 0:
            time.sleep(remaining_time)

        if keyboard.is_pressed('g'):
            stop = True
    
    #to do: alle fietsen terugbrengen naar stations

    #save data for next time
    if (save == True):
        sim_save = {"runningTime": time.time() - sim_start, "sim_seconds": sim_minutes, "riders": riders, "walking": walking, "bikesInUse": bikesInUse, "almost_empty": almost_empty, "almost_full": almost_full, "currently_transp": currently_transp, "available_transp": available_transp}
        dict_to_pickle(saveTo, sim_save)
        dict_to_json("site_info.json", site_info)
        dict_to_json("userInfo.json", userInfo)
        save_data()
    
loop(60, 'sim.pkl')