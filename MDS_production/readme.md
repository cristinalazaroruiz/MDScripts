# MOLECULAR DYNAMICS SIMULATION PRODUCTION

This folder contains scripts to run Molecular Dynamics (MD) simulations using GROMACS.

- *DM.py*: This script runs basic molecular dynamics steps prior to production, including solvation, ionization and energy minimization. It accepts a GRO file (for protein-ligand complexes previously created ) or a PDB file (from which it will generate the GRO and topology files).
- 
**WARNING**: this script requires GROMACS and GROMACS WRAPPER to be installed on your system. 
