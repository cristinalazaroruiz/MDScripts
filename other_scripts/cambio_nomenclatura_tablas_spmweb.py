#NOTE: this script need pandas to be installed
import pandas as pd
import openpyxl

###############################################################################
#                           FUNCTIONS
###############################################################################
    
def read_table(table):
    
    try:
        df = pd.read_excel(table)
        
        return df
    
    except Exception as e:
        print(f"Unable to open {table}")
        print(f"Error details: {e}")
        return None
    
# get information from table and change
# we want 8rfn nomenclature:
#   Chain A goes from Val2 to Lys274
#   Chain B goes from Val275 to Arg546

# 8rfm nomenclature is:
#   Chain A goes from Val2 to Arg273
#   Chain B goes from Gly274 to Arg544


# So, if we want only to have two different residues (Arg273 and Gly274) that are only present in WT 8rfm
# we want to add two positions to Lys274



def get_information_script(df):
    
    if df is None:
        return None
    try:
        # Para Residue_1
        df.loc[df["Residue_1"] >= 274, "Residue_1"] += 2
        
        # Para Residue_2
        df.loc[df["Residue_2"] >= 274, "Residue_2"] += 2
        
        return df
    
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return df 
        

###############################################################################
#                           FUNCTIONS
###############################################################################

while True:
    
    print("¿What do you want to do?")
    print("(1) >> Change 8rfm nomenclature to adapt to the 8rfn one")
    print("(2) >> Exit")
    n = input("Choose (enter 1 o 2): ")
    
    if n == "1":
        
        print("***WARNING***")
        print("This script needs pandas and openpyxl to be installed in your system")
        
        #Ask user which file must be used
        script = input("table file name with xlsx extension (path): ")
        
        #Apply functions
        df = read_table(script)
        df_modificado = get_information_script(df)
        
        try:
            df_modificado.to_excel(f"changed_{script}",  index=False)
            print(f"✅ changed_{script} created successfully")
        
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
