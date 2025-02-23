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
global index_sheet


def f_sync_newfolder():
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



def f_address_input_networks():
    # OK
    global L_address_input_networks, L_name_networks
    
    # To read all networks file in the "Networks" folder
    if DICT_NETWORKS["L_NAME_NET"][0] == "ALL_NETWORKS":
        #make a list of all xlsx files' addresses from the "Networks" folder
        L_address_input_networks = list(filter(re.compile(".*xlsx").match, os.listdir(NET_DIR)))
        # Some times there are more than one (e.g. 4) xlsx file in the "Networks" folder.
        # Since we did not know their names before reading them, we need to make a list in the as length as long as their count.
        # E.g. if there are 4 xlsx files, we need:["ALL_NETWORKS","ALL_NETWORKS","ALL_NETWORKS","ALL_NETWORKS"]
        # Becouse, in the for loop, eache time it check the network's name(i.e. "ALL_NETWORKS") and reed the sheet number from .jason file.
        # In the .jason file, we wrote sheet numbers like: "ALL_NETWORKS : [2,4,7]"; which applies for all the networks in the "Networks" folder.
        L_name_networks = ["ALL_NETWORKS"] * len(L_address_input_networks)

    else:
        # If we want just specific networks files from the "Networks" folder
        # This list would be used in the for loop.
        L_name_networks = DICT_NETWORKS["L_NAME_NET"]
        # make a copy to use it since the name and address is the same and was saved in the .json file.s
        L_address_input_networks = L_name_networks.copy()
    
    

def f_read_graph(g_name):
    # OK
    global DF_GRAPH, NUM_NODES
    
    DF_GRAPH = pd.read_excel(NET_DIR + g_name, sheet_name = index_sheet)
    # To count the exact number of nodes because the "DF_GRAPH" is not a graph! it ia a dataframe.
    NUM_NODES = max(max(DF_GRAPH["source"]), max(DF_GRAPH["target"])) + 1
     
 
    
    
def arr_type(the_type, model_name, case, address_net):
    
    if(the_type != "LIKE_OTHER_MODEL"):
        arr_value = np.zeros(NUM_NODES)
        
        if(the_type     == "NORMAL_RANDOM"):
            key_mean    = "MEAN" + case
            key_std     = "STD" + case
            random_std  = DICT_MODEL[model_name][key_std]
            random_mean = DICT_MODEL[model_name][key_mean]
            arr_value   = np.random.normal(random_mean, random_std, NUM_NODES)
            
        elif(the_type   == "UNIF_RANDOM"):
            key_max     = "MAX" + case
            key_min     = "MIN" + case
            random_max  = DICT_MODEL[model_name][key_max]
            random_min  = DICT_MODEL[model_name][key_min]
            arr_value   = np.random.uniform(low = random_min, high = random_max, size = NUM_NODES)
        
        elif(the_type   == "ALL_SAME_RANDOM"):
            key_max     = "MAX" + case
            key_min     = "MIN" + case
            random_max  = DICT_MODEL[model_name][key_max]
            random_min  = DICT_MODEL[model_name][key_min]
            arr_value   = arr_value + np.random.uniform(low = random_min, high = random_max)
            
        elif(the_type   == "ALL_SAME_FIXED"):
            key_value   = "VALUE" + case
            fixed_value = DICT_MODEL[model_name][key_value]
            arr_value   = arr_value + fixed_value
            
        elif(the_type   == "GIVEN_LIST"):
            key_value   = "VALUE" + case
            fixed_value = DICT_MODEL[model_name][key_value]
            arr_value   = arr_value + fixed_value
            
        elif(the_type   == "GIVEN_COLUMN"):
            key_scale       = "SCALE" + case
            key_scale_value = "VALUE_SCALE" + case
            key_sheet       = "SHEET_XLSX" + case
            key_column      = "COLUMN" + case
            
            sheet_xlsx  = DICT_MODEL[model_name][key_sheet]
            column_xlsx = DICT_MODEL[model_name][key_column]
            scale       = DICT_MODEL[model_name][key_scale]
            
            if(sheet_xlsx == "NODES"):
                arr_value = pd.read_excel(NET_DIR + address_net, sheet_name = index_sheet-1)[column_xlsx]
                if (scale == "MAX"):
                    value_scale   = DICT_MODEL[model_name][key_scale_value]
                    arr_value = np.array(arr_value) / np.max(arr_value) * value_scale
                elif (scale == "MEAN"):
                    value_scale   = DICT_MODEL[model_name][key_scale_value]
                    arr_value = np.array(arr_value) / np.mean(arr_value) * value_scale
                else:
                    arr_value = np.array(arr_value)

                
    elif(the_type == "LIKE_OTHER_MODEL"):
        key_like  = "LIKE_MODEL" + case
        like_model_index = DICT_MODEL[model_name][key_like]
        if (case == "_K"):
            arr_value = arr_models_k[like_model_index,:]
        if (case == "_G"):
            arr_value = arr_models_g[like_model_index,:]
        elif (case == "_OMEGA"):
            arr_value = arr_models_omega[like_model_index,:]
        elif (case == "_PHI"):
            arr_value = arr_models_phi[like_model_index,:]
        elif (case == "_AMPLI"):
            arr_value = arr_models_ampli[like_model_index,:]
        elif (case == "_NOISE"):
            arr_value = arr_models_noise[like_model_index,:]
            
    return arr_value
    


def f_k_models_op_sync(model, step):
    global arr_models_op_coherence, arr_models_op_phase
    
    parameter_real = sum(np.cos(arr_models_phi[model,:])) / NUM_NODES
    parameter_img = sum(np.sin(arr_models_phi[model,:])) / NUM_NODES

    arr_models_op_phase[model, step] = np.arctan2(parameter_img, parameter_real) % (2 * np.pi)
    arr_models_op_coherence[model, step] = np.sqrt(parameter_real**2 + parameter_img**2)



def f_initialize_models(address_net):
    #OK
    global list_dict_phi, list_dict_noise
    global arr_models_k, arr_models_g, arr_models_omega, arr_models_phi
    global arr_models_ampli, arr_models_noise, temp_arr_phi
    global arr_models_op_phase, arr_models_op_coherence

    list_dict_phi           = []
    list_dict_noise         = []
    arr_models_k            = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_g            = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_omega        = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_phi          = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_ampli        = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_noise        = np.zeros((NUM_MODELS, NUM_NODES))
    temp_arr_phi            = np.zeros((NUM_MODELS, NUM_NODES))
    arr_models_op_phase     = np.zeros((NUM_MODELS, NUM_TOTAL_STEPS))
    arr_models_op_coherence = np.zeros((NUM_MODELS, NUM_TOTAL_STEPS))

    for m in range(NUM_MODELS):
        
        model_name = LIST_MODELS[m]
        
        # To use the type of parameters
        k_type      = DICT_MODEL[model_name]["TYPE_K"]
        g_type      = DICT_MODEL[model_name]["TYPE_G"]
        omega_type  = DICT_MODEL[model_name]["TYPE_OMEGA"]
        phi_type    = DICT_MODEL[model_name]["TYPE_PHI"]
        #ampli_type  = DICT_MODEL[model_name]["TYPE_AMPLI"]
        noise_type  = DICT_MODEL[model_name]["TYPE_NOISE"]
        
        # To set initial values based on .jason file
        arr_models_k[m,:]       = arr_type(k_type, model_name, "_K", address_net)
        arr_models_g[m,:]       = arr_type(g_type, model_name, "_G", address_net)
        arr_models_omega[m,:]   = arr_type(omega_type, model_name, "_OMEGA", address_net)
        arr_models_phi[m,:]     = arr_type(phi_type, model_name, "_PHI", address_net)
        #arr_models_ampli[m,:]   = arr_type(ampli_type, model_name, "_AMPLI", address_net)
        arr_models_noise[m,:]   = arr_type(noise_type, model_name, "_NOISE", address_net)
        
        # to create a dict for saving as xlsx
        list_dict_phi.append(dict())
        list_dict_noise.append(dict())

        #To save the phi of staep 0 (Noise should be saved from step 1!)
        list_dict_phi[m]["0"]   = arr_models_phi[m,:].copy()
        
        # To calculate the ort\der parameter of step 0!
        f_k_models_op_sync(m, 0)

























def f_set_models_on_graphs():

    global index_sheet

    f_address_input_networks()
    
    for rep in range(DICT_RUN["TOTAL_REPEAT"]):
        print(f"\n\n\tRepeat: {rep+1} of {DICT_RUN['TOTAL_REPEAT']}")
        print(f"\n\t\tRunning {NUM_MODELS} Model(s) at the same time on:")
        network_counter = 1
        # loop on all the networks that we want to put the models on them.
        for net in range(len(L_name_networks)):
            # To read the sheet number from .jason file
            for in_sh in DICT_NETWORKS[L_name_networks[net]]:
                index_sheet = in_sh
                # Read the "index_sheet" from the "net" file
                f_read_graph(L_address_input_networks[net])
                f_initialize_models(L_address_input_networks[net])
                f_select_feature(L_address_input_networks[net])
                f_create_result_xlsx(network_counter, rep, L_address_input_networks[net])
                f_start_sync()
                f_desync_run()
                f_end_sync(L_address_input_networks[net])
                f_update_result_xlsx()
                network_counter += 1


    
def f_main():
    f_sync_newfolder()
    f_read_parameters()
    f_set_models_on_graphs()
    
    END_TIME = f'{datetime.now().strftime("%H:%M:%S")}'
    print("\n-----------------------------------------------")
    print(f"\nRun id: {TIME_ID}")
    print(f"\nStart time: {START_TIME}")
    print(f"End time: {END_TIME}")
    print("\n-----------------------------------------------")


f_main()
