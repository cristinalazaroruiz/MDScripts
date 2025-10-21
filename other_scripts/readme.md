# Explanation

Apart from the previous scripts, which can be useful for the basic steps during MD Simulation preparation and execution, there are other issues that may arise during the process. This folder contains additional scripts can find other scripts to handle less common situations: 

> **cambiar_cadenas.py** > if you used MODELLER to build your protein and it is a homodimer, you may end up with two chains (A and B) whose residue numbering differs. You can use this script to o make the residue numbering in both chains consistent (make sure both chains are named A and B and change if necessary). 

> **modificacion_pdbs.py** > contrary, you may need each chain of your homodimer with different nomenclature (chain B starting from last chain A residue). In this case, you can use this script. 