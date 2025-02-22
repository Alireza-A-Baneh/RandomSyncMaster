import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime
import json
import os
import re
import openpyxl
import shutil


def f_net_newfolder():
    global TIME_ID, START_TIME
    global CODE_DIR, DATASETS_DIR, DEST_DIR, RUN_NUMBER
    
    print("\n-----------------------------------------------")
    TIME_ID = f'{datetime.now().strftime("%y%m%d-%H%M%S")}'
    START_TIME = f'{datetime.now().strftime("%H:%M:%S")}'
    print(f"\nRun id: {TIME_ID}")
    print(f"\nStart time: {START_TIME}")
    print("\n-----------------------------------------------")

    # Adding \.. to the end of the path. so abspath is the parrent folder

    # D:\Academic\Research\BrainSyncMaster\010-Networks\Code
    CODE_DIR = os.path.dirname(os.path.realpath(__file__))
    # D:\Academic\Research\BrainSyncMaster\010-Networks
    PARENT_DIR = os.path.abspath(CODE_DIR+"\\..")
    # D:\Academic\Research\BrainSyncMaster\
    PROJECT_DIR = os.path.abspath(CODE_DIR+"\\..\\..")
    # D:\Academic\Research\BrainSyncMaster\010-Networks\DATASETS\
    DATASETS_DIR = PARENT_DIR + "\\DATASETS\\"
    # D:\Academic\Research\BrainSyncMaster\Outputs\
    dest_dir = PROJECT_DIR + "\\Outputs\\"

    # Creat new folder (How many runs have been ran)
    L_pre_runs = list(filter(re.compile("Net ").match, os.listdir(dest_dir)))

    if len(L_pre_runs) != 0:
        # finding max run number
        RUN_NUMBER = (int((re.findall(" [0-9]{3} ", L_pre_runs[-1]))[0])) + 1
        # naming the folder
        if RUN_NUMBER < 10:
            RUN_NUMBER = f'Net 00{RUN_NUMBER}'
        elif RUN_NUMBER < 100:
            RUN_NUMBER = f'Net 0{RUN_NUMBER}'
        else:
            RUN_NUMBER = f'Net {RUN_NUMBER}'
    # if this is the first run
    else:
        RUN_NUMBER = 1
        RUN_NUMBER = f'Net 00{RUN_NUMBER}'


    DEST_DIR = os.path.join(f'{dest_dir}', f"{RUN_NUMBER} (id = {TIME_ID})")
    os.makedirs(DEST_DIR)   

    # To copy this code and json file destination folder
    shutil.copytree(PARENT_DIR + "\\Code" , DEST_DIR+"\\Initial Parameters", dirs_exist_ok=True)



def f_read_initial_data():
    global DICT_RUN, DICT_DATASETS, DICT_NETWORK
    
    with open("Initial Networks Parameters.json", "r") as json_file:
        J_DATA      = json.load(json_file)
        
    DICT_RUN        = J_DATA["RUN"]
    DICT_DATASETS   = J_DATA["DATASETS"]
    DICT_NETWORK    = J_DATA["NETWORKS"]




def f_graph_weight(w_type, w_const, w_min, w_max, num_edges):
    
    arr_weight = np.zeros(num_edges)
    
    if(w_type == "NORMAL_RANDOM"):
        mu = (w_max + w_min) / 2
        sigma = (w_max - w_min) / 3
        arr_weight = np.random.normal(mu, sigma, num_edges)
        arr_weight[(arr_weight < w_min )|(arr_weight > w_max)] = mu

    elif(w_type == "UNIF_RANDOM"):
        arr_weight = np.random.uniform(low = w_min, high = w_max, size = num_edges)

    elif(w_type == "CONSTANT"):
        arr_weight = arr_weight + w_const
        print(arr_weight)

    arr_weight = np.array(list(map(int, arr_weight)))

    return arr_weight






















def f_main():
    
    global END_TIME
    
    f_net_newfolder()
    f_read_initial_data()
    
    if(DICT_RUN["READ_FROM"] == "DATASETS"):
        f_read_dataset()
        
    elif(DICT_RUN["READ_FROM"] == "NETWORKS"):
        f_creat_networks()






















f_net_newfolder()

