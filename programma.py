import time
import sys
from parsers import json_to_dict, dict_to_json
from sim import loop

#rules: 
# sim speed >= 1
# warning if savefile with same name already exists

def startSim(simSpeed, saveFile, saveTo):
    print("\n\nsimulation starting...\n  tip: hold 'ctrl' to manually mount or return a bike (pause menu)\n  tip: hold 'G' to quit and (if enabled) save to file\n\n\n")
    time.sleep(1.5)
    loop(simSpeed, saveFile, saveTo)

def askOption(question, optionList):
    keuze = input(question)
    while (keuze not in optionList):
        print(f"\n{keuze} is geen optie")
        keuze = input(question)
    return keuze


#start code
simSettings = json_to_dict("settings.json")
if (len(simSettings) == 0):
    simSpeed = 1
    saveFile = None
    saveTo = "sim.pkl"
else:
    simSpeed = simSettings["simSpeed"]
    saveFile = simSettings["saveFile"]
    saveTo = simSettings["saveTo"]

if ("-s" not in sys.argv):
    print("\n-- start menu --\n")
    print(f"huidige intellingen:")
    if (saveFile is None):
        print("- bij start: start nieuwe simulatie")
    else:
        print(f"- bij start: ga verder van saveFile: {saveFile}")

    if (saveTo is None):
        print("- bij afsluit: simulatie niet opslaan")
    else:
        print(f"- bij afsluit: simulatie opslaan naar {saveTo}")

    if (simSpeed == 1):
        print("- simulatiesnelheid: realtime")
    else:
        if (simSpeed < 60):
            print(f"- simulatiesnelheid: {simSpeed}x realtime (1s = {simSpeed}s)")
        else:
            print(f"- simulatiesnelheid: {simSpeed}x realtime (1s = {simSpeed/60} minutes)")

    print("\n1. doorgaan met deze instellingen\n2. intellingen aanpassen")

    startKeuze = askOption("maak je keuze: ", ["1","2"])

    #changing settings if user chooses option 2
    if(startKeuze == "2"):
        startFromFile = askOption("wenst u verder te gaan vanuit een eerder opgeslagen save? (j/n) ", ["j","n"])
        if (startFromFile == 'j'):
            openFrom = input("vanuit welk bestand wilt u verder gaan? ")
            while (openFrom in ["data.pkl", "site_info.json", "userInfo.json", "velo.json", "names.json", "settings.json"]):
                print(f"\n{openFrom} is geen saveFile, gelieve een ander bestand te kiezen")
                openFrom = input("vanuit welk bestand wilt u verder gaan? ")
            saveFile = openFrom
        else:
            saveFile = None
        
        saveProgress = askOption("wenst u de simulatie op te slaan bij afsluit? (j/n) ", ["j","n"])
        if (saveProgress == 'j'):
            saveFileChoice = input('naar welk bestand wilt u opslaan? (antwoord met "[bestandsnaam].pkl") ')
            while (saveFileChoice in ["data.pkl", "site_info.json", "userInfo.json", "velo.json", "names.json", "settings.json"]):
                print(f"\nbestandsnaam {saveFileChoice} is niet toegestaan, gelieve een andere bestandsnaam te kiezen")
                saveFileChoice = input("naar welk bestand wilt u opslaan? ")
            saveTo = saveFileChoice
        else:
            saveTo = None
        
        speed = int(input("met welke snelheid wilt u de simulatie runnen? (1 => realTime, 60 => 1s=1m) (snelheden groter dan 300 hebben weinig nut) "))
        while (speed <= 0) or (speed > 1000):
            print("gelieve een simulatiesnelheid groter dan 0 en kleiner dan 1000 te kiezen")
            speed = int(input("met welke snelheid wilt u de simulatie runnen? (1 => realTime, 60 => 1s=1m) (snelheden groter dan 300 hebben weinig nut) "))
        simSpeed = speed

    #saving settings
    simSettings = {"simSpeed": simSpeed, "saveFile": saveFile, "saveTo": saveTo}
    dict_to_json("settings.json", simSettings)

#starting simulation
startSim(simSpeed, saveFile, saveTo)


