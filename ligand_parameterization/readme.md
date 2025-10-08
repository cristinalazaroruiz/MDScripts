# PARAMETERIZATION

Ligand parameterization is a crucial process in MD simulations. Here, we provide some scripts to simplify the process and generate the necessary files for running MD within GROMACS. 

*Steps for ligand parameterization are:*

1- **Ligand protonation** (manually if possible with PyMOL, AVOGADRO...) and generation of PDB/MOL2 file. 

2- **Generation of Gaussian input (.COM file) from PDB/MOL2 file**. You can use script prepare_ligands.sh to simplify the process (remember to customize your Gaussian header). 

3-**Transformation of GAUSSIAN output (.LOG) to MOL2 file**, to preserve the correct geometry. You can use the script change_log_mol2.sh for this. 

4- This MOL2 file from GAUSSIAN may have lost its correct nomenclature, you can use script mol2_nomenclature.py to get back the correct naming. A new MOL2 file, named nomenclature_file.mol2 will be created. 

5- Aditionally, this MOL2 file may have a column were the ligand name is "UNL". In protein-ligand dynamics with more than one ligand, a conflict can appear if all ligands are named "UNL". To solve this problem, you can use change_UNL.script to change "UNL" for a customized name for each ligand (this name should be the same that is present in the original MOL2 with the correct configuration of the ligand).

5-**Transformation of GAUSSIAN output (.FCHK) to CHG file**, using multifwn to calculate suitable charges for your ligand.

6- **Replacing MOL2 charges  with chg charges in your MOL2 file (nomenclature_file.MOL2)** . You can use change_charges.py to simplify the step. A new MOL2 file, named ready_file.mol2 will be created. 

7- **Parameterization with ANTECHAMBER (via ACEPYPE) of the ready_file.mol2 structure**. You can use acpype.sh to simplify the process. 

This will generate a new folder containing all the necessary ligand files to run MD simulation with GROMACS. 

8. **Transformation of original and protonated ligand files (MOL2 or PDB) to GRO format.** You can use mol2pdb.sh to transform MOL2 files to PDB files and then pdb2gmx.sh to transform PDB files to GRO files. 

*NOTE 1: Once the parameterization is done, the files generated with ACEPYPE can be reused for multiple simulations of the same molecules. However, if different GRO files (from the same ligand) are generated with an atom order that does not match the corresponding ITP file, errors may occur. In that case, you can use the script order_itp_gro.py to reorder atoms in the GRO file so that they match the order defined in the ITP file.*

*Note 2: When executing bash scripts in Windows environments (like WSL) errors may occur if the scripts are saved with Windows-style line endings (CRLF). To fix this, you can convert them to Unix-style endings (LF) using the following command:*

> sed -i 's/\r$//' script.sh









