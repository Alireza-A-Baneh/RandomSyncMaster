from datetime import datetime
import pandas as pd
import numpy as np
import openpyxl
import shutil
import json
import os
import re
import random


global START_TIME, TIME_ID
global CODE_DIR, NET_DIR, DEST_DIR
global DICT_RUN
global DICT_MODEL, DICT_NETWORKSglobal, list_result_xlsx_path, list_dict_phi
global DF_GRAPH, NUM_NODES
global NUM_MODELS, NAMES_MODELS
global arr_models_omega, arr_models_phi, arr_models_ampli
global arr_models_op_coherence, arr_models_op_phase



def f_net_newfolder():
    global TIME_ID, START_TIME
    global CODE_DIR, NET_DIR, DEST_DIR, RUN_NUMBER
    
    print("\n-----------------------------------------------")
    TIME_ID = f'{datetime.now().strftime("%y%m%d-%H%M%S")}'
    START_TIME = f'{datetime.now().strftime("%H:%M:%S")}'
    print(f"\nRun id: {TIME_ID}")
    print(f"\nStart time: {START_TIME}")
    print("\n-----------------------------------------------")

    # Adding \.. to the end of the path. so abspath is the parrent folder

    # D:\Academic\Research\BrainSyncMaster\020-Synchronization\Code
    CODE_DIR = os.path.dirname(os.path.realpath(__file__))
    # D:\Academic\Research\BrainSyncMaster\020-Synchronization
    PARENT_DIR = os.path.abspath(CODE_DIR+"\\..")
    # D:\Academic\Research\BrainSyncMaster\
    PROJECT_DIR = os.path.abspath(CODE_DIR+"\\..\\..")
    # D:\Academic\Research\BrainSyncMaster\020-Synchronization\Networks\
    NET_DIR = PARENT_DIR + "\\Networks\\"
    # D:\Academic\Research\BrainSyncMaster\Outputs\
    dest_dir = PROJECT_DIR + "\\Outputs\\"

    # Creat new folder (How many runs have been ran)
    L_pre_runs = list(filter(re.compile("Sync ").match, os.listdir(dest_dir)))

    if len(L_pre_runs) != 0:
        # finding max run number
        RUN_NUMBER = (int((re.findall(" [0-9]{3} ", L_pre_runs[-1]))[0])) + 1
        # naming the folder
        if RUN_NUMBER < 10:
            RUN_NUMBER = f'Sync 00{RUN_NUMBER}'
        elif RUN_NUMBER < 100:
            RUN_NUMBER = f'Sync 0{RUN_NUMBER}'
        else:
            RUN_NUMBER = f'Sync {RUN_NUMBER}'
    # if this is the first run
    else:
        RUN_NUMBER = 1
        RUN_NUMBER = f'Sync 00{RUN_NUMBER}'


    DEST_DIR = os.path.join(f'{dest_dir}', f"{RUN_NUMBER} (id = {TIME_ID})")
    os.makedirs(DEST_DIR)   

    # To copy this code and json file destination folder
    shutil.copytree(PARENT_DIR + "\\Code" , DEST_DIR+"\\Initial Parameters", dirs_exist_ok=True)


def f_read_parameters():
    global DICT_NETWORKS, DICT_RUN, DICT_MODEL
    global NUM_MODELS, LIST_MODELS, NUM_TOTAL_STEPS

    with open("Initial Sync Parameters.json", "r") as json_file:
        DATA = json.load(json_file)
        
    #Seperate data from json file in different dictionaries to (Easy to Access)
    DICT_NETWORKS   = DATA["NETWORKS"]
    DICT_RUN        = DATA["Run"]
    DICT_MODEL      = DATA["MODELS"]
    
    NUM_MODELS = DICT_MODEL["FIXED_PAR"]["NUM_MODELS"]
    LIST_MODELS = DICT_MODEL["FIXED_PAR"]["L_MODELS"]
    NUM_TOTAL_STEPS = DICT_RUN["START_SYNC_NUM_STEPS"] + DICT_RUN["De_SYNC_NUM_STEPS"] + DICT_RUN["END_SYNC_NUM_STEPS"]

    







































f_net_newfolder()
