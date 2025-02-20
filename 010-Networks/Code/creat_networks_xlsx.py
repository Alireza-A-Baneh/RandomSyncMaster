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

f_net_newfolder()

