#NOTE: this script need pandas to be installed
import pandas as pd
import re
import numpy as np
import openpyxl

###############################################################################
#                           FUNCTIONS
###############################################################################

#read file
def read_script(script):
    lineas = []
    try:
        with open(script, mode = "r", encoding = "utf-8" ) as file:
            lineas = file.readlines()
        
        return lineas
    
    except Exception as e:
        print(f"Unable to open {script}")
        print(f"Error details: {e}")
        return []
        
    
#get information for script
def get_information_script(lines):

    dict_residue_radius = {}
    dict_pair_stick = {}

    current_stick_radius = None

    for raw in lines:
        linea = raw.strip()

        # sphere_scale
        # Example: set sphere_scale,0.49279019466474405, SPM_8rfn_r10 and resi 101
        if linea.startswith("set sphere_scale"):
            m = re.search(r"set\s+sphere_scale,([\d\.eE+-]+).*resi\s+(\d+)", linea)
            if m:
                radius = float(m.group(1))
                residue = m.group(2)
                dict_residue_radius[residue] = radius
            continue

        # stick_radius
        # Example: set stick_radius,0.43876896772814705, SPM_8rfn_r10
        if linea.startswith("set stick_radius"):
            m = re.search(r"set\s+stick_radius,([\d\.eE+-]+)", linea)
            if m:
                current_stick_radius = float(m.group(1))
            continue

        # create with resi A+B
        # Example: create SPM_8rfn_r10, name ca and resi 101+102 and 8rfn_r1
        if linea.startswith("create") and current_stick_radius is not None:
            m = re.search(r"resi\s+(\d+)\+(\d+)", linea)
            if m:
                r1, r2 = m.group(1), m.group(2)
                pair = f"{r1}/{r2}"
                dict_pair_stick[pair] = current_stick_radius
                # reset: we assume that stick_radius corresponded with that create
                current_stick_radius = None
            else:
                print(f"Warning: 'create' line ignored (unexpected format): {linea}")

    return dict_residue_radius, dict_pair_stick

        
#create separate dataframes for radiuos and sticks
def create_dataframes(dict_residue_radius, dict_pair_stick , script):
    try:
        df_radius = pd.DataFrame(list(dict_residue_radius.items()), columns=["Residue", "Sphere_Radius"])
        df_sticks = pd.DataFrame(list(dict_pair_stick.items()), columns=["Residue_Pair", "Stick_Radius"])
        
        return df_radius, df_sticks
        
    except Exception as e:
        print(f"Unable to write final dataframe for script {script}")
        print(f"Error details: {e}")


#merge both dataframes
def merge_df(dict_residue_radius, dict_pair_stick):
    try:
        rows = []

        # go down each pair of residues
        for pair, stick in dict_pair_stick.items():
            r1, r2 = pair.split("/") #split both residues
            r1_radius = dict_residue_radius.get(r1, np.nan) #radius from the other dict
            r2_radius = dict_residue_radius.get(r2, np.nan) # radius from the other dict

            rows.append({
                "Residue_1": int(r1),
                "Sphere_Radius_1": r1_radius,
                "Residue_2": int(r2),
                "Sphere_Radius_2": r2_radius,
                "Stick_Radius": stick
            })

        # crear DataFrame y ordenar por Residue_1
        if rows:
            df_merged = pd.DataFrame(rows)
            df_merged= df_merged.sort_values("Residue_1").reset_index(drop=True)
        else:
            #Empty rows
            df_merged = pd.DataFrame(columns=["Residue_1", "Sphere_Radius_1", "Residue_2", "Sphere_Radius_2", "Stick_Radius"])

        return df_merged
        
        
    except Exception as e:
        print("Unable to merge both dataframes")
        print(f"Error details: {e}")
        return pd.DataFrame(columns=["Residue_1", "Sphere_Radius_1", "Residue_2", "Sphere_Radius_2", "Stick_Radius"])
    
###############################################################################
#                           FUNCTIONS
###############################################################################

while True:
    
    print("¿What do you want to do?")
    print("(1) >> Get radius and stick information from a pml script")
    print("(2) >> Exit")
    n = input("Choose (enter 1 o 2): ")
    
    if n == "1":
        
        print("***WARNING***")
        print("This script needs pandas, numpy and openpyxl to be installed in your system")
        
        #Ask user which file must be used
        script = input("pml file name (path): ")
        
        #Apply functions
        lineas = read_script(script)
        dict_residue_radius, dict_pair_stick = get_information_script(lineas)
        df_radius, df_sticks = create_dataframes(dict_residue_radius, dict_pair_stick, script)
        df_merged = merge_df(dict_residue_radius, dict_pair_stick)
        
        try:
            df_merged.to_excel(f"{script}_information.xlsx",  index=False)
            print(f"✅ {script}_information.xlsx created successfully")
        
        except Exception as e:
            print(f"❌ Error in creating new excel file for {script}")
            print(f"Error details: {e}")

        
    elif n == "2":
        print("Exiting the program...")
        print("-----------------------------------------------------------------------------")
        print("-----------------------------------------------------------------------------")
        break 
    
    else:
        print("Invalid input, please enter 1 or 2")



















        


