# ANALYSIS OF MD SIMULATIONS

In this folder you can find scripts to simplify and automate the analysis of results from GROMACS MD simulations.

- *xpm2dat.py* > this script is based on **GROMACS WRAPPER**, a Python framework for GROMACS. It uses GROMACS WRAPPER functions and classes to convert GROMACS XPM files—commonly produced for matrices such as distance matrices generated with *gmx mdmat*—into plain DAT files for further analysis.
- *covarmat2cormat.py* > This script takes a covariance matrix in XPM format (calculated with **gmx covar**) and transforms it into a correlation matrix in DAT format. Version 2 of the script returns the correlation matrix in AMBER style, meaning the values are per atom instead of per individual coordinate (x, y, z). 

- *analisis.sh* > this script uses **cpptraj**, from ambertools to obtain the distance matrix and correlation matrix in DAT an NPY format. Note that you need AMBER topology (prmtop) to use this script. You can obtain it from GROMACS topology file (TOP) with *parmed* (specifically *gromber*). You also need python an numpy installed in your system.

- *rmsd_analysis.R* > This R script plots XVG files from GROMACS (RMSD, RMSF, etc.)

- *gromacs_commands.sh* > this bash script allows running different gromacs commands for processing files (removing PBCs, calculating RMSD, distances...). 

- *analisis_script_spmweb* > python script to analyze results from SPM Web Server (https://spmosuna.com/) in order to get a table with numerical values of significance of residue radius and sticks. 

- *GMX_MMPBSA_launcher+analisis_GB.in* > files to launch a free binding energy calculation of protein-ligand complex with gmx_MMPBSA tool. 

- *clustering.Rmd* > Rmarkdown defining a protocol to cluster paths generated with SPMweb and analyzed with the tables created with  *analisis_script_spmweb*

- *load_trajectories_pymol.py* > a script to illustrate how to load several gromacs trajectories in pymol automatically, using python syntaxis. 