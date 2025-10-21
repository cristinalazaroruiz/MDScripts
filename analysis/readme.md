# ANALYSIS OF MD SiMULATIONS

In this folder you can find scripts to simplify and automate the analysis of results from GROMACS MD simulations.

- *xpm2dat.py* > this script is based on **GROMACS WRAPPER**, a Python framework for GROMACS. It uses GROMACS WRAPPER functions and classes to convert GROMACS XPM files—commonly produced for matrices such as distance matrices generated with *gmx mdmat*—into plain DAT files for further analysis.
- *covarmat2cormat.py* > This script takes a covariance matrix in XPM format (calculated with **gmx covar**) and transforms it into a correlation matrix in DAT format. Version 2 of the script returns the correlation matrix in AMBER style, meaning the values are per atom instead of per individual coordinate (x, y, z). 

- *analisis.sh* > this script uses **cpptraj**, from ambertools to obtain the distance matrix and correlation matrix in DAT an NPY format. Note that you need AMBER topology (prmtop) to use this script. You can obtain it from GROMACS topology file (TOP) with *parmed* (specifically *gromber*). You also need python an numpy installed in your system. 
