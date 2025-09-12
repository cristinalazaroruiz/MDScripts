# PARAMETERIZATION

Ligand parameterization is a crucial process in MD simulations. Here, we provide some scripts to simplify the process and generate the necessary files for running MD within GROMACS. 

*Steps for ligand parameterization are:*

1- **Ligand protonation** (manually if possible) and generation of pdb/mol2 file. 

2- **Generation of Gaussian input (.com file) from pdb/mol2 file**. You can use script prepare_ligands.sh to simplify the process (remember to customize your Gaussian header). 

3-**Transformation of GAUSSIAN output (.log) to mol2 file**, to preserve the correct geometry. You can use the script change_log_mol2.sh for this. 

4-**Transformation of GAUSSIAN output (.fchk) to chg file**, using multifwn to calculate suitable charges for your ligand.

5- **Replacing mol2 charges with chg charges in your mol2 file**. You can use change_charges.py to simplify the step. A new mol2 file, named ready_file.mol2 will be created. 

6- **Parameterization with ANTECHAMBER (via ACEPYPE) of the ready_file.mol2 structure**. You can use acpype.sh to simplify the process. 

This will generate a new folder containing all the necessary ligand files to run MD simulation with GROMACS. 


