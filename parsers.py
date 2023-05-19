import json
import pickle

def json_to_dict(source):
    dict = {}
    #try to open JSON file with already entered pages (if the file exists)
    try:
        with open(f"data/{source}", "r") as f:
            dict = json.load(f)
    except:
        #leave dictionary empty/unchanged if no JSON is found
        print(f"no file named {source} found: returning empty dict")
        dict = dict
    return dict

def dict_to_json(filename, dict):
    with open(f"data/{filename}", 'w') as file:
        # Use json.dump() to serialize and save the data
        json.dump(dict, file, indent=4)

def pickle_to_dict(source):
    dict = {}
    #try to open JSON file with already entered pages (if the file exists)
    try:
        with open(f"data/{source}", "rb") as f:
            dict = pickle.load(f)
    except:
        #leave dictionary empty/unchanged if no JSON is found
        print(f"no file named {source} found: returning empty dict")
        dict = dict
    return dict

def dict_to_pickle(filename, dict):
    with open(f"data/{filename}", 'wb') as file:
        # Use json.dump() to serialize and save the data
        pickle.dump(dict, file)

def vals(list):
    vals = [x for x in list if x is not None]
    return vals