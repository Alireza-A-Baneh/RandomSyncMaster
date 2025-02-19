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
    #"D:\\Academic\\Thesis\\Modeling\\Networks\\Code"
    CODE_DIR = os.path.dirname(os.path.realpath(__file__))
    print(CODE_DIR)
    print(os.listdir())
    print('test_directory' in os.listdir())
    par_dir = os.path.abspath(os.path.join(CODE_DIR, os.pardir))
    print(par_dir)

    #"D:\\Academic\\Thesis\\Modeling\\Networks"

    par_dir = os.path.abspath(os.path.join(CODE_DIR, os.pardir))
    #"D:\\Academic\\Thesis\\Modeling\\Networks\\Result"
    # DEST_DIR = par_dir + "\\Result" 
    DATASETS_DIR = par_dir + "\\DATASETS\\"
    DEST_DIR = par_dir
    print(CODE_DIR)
    print(DATASETS_DIR)
    print(DEST_DIR)
    
    # Creat new folder (How many runs have been ran)
    L_pre_runs = list(filter(re.compile("Net ").match, os.listdir(DEST_DIR)))

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


    DEST_DIR = os.path.join(f'{DEST_DIR}', f"{RUN_NUMBER} (id = {TIME_ID})")
    os.makedirs(DEST_DIR)   

    # To copy this code and json file destination folder
    shutil.copytree(par_dir + "\\Code" , DEST_DIR+"\\Initial Parameters", dirs_exist_ok=True)

f_net_newfolder()

