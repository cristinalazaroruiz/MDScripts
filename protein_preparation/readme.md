# PROTEIN PREPARATION

Within MD Simulations, a very important step is the preparation of the protein 3D structure. We have to make sure that:

-There are not missing residues (especially if the structure has been obtained experimentally, like crystallography). To do so, you can use script residue_check.py to extract PDB sequence. Afterwards, you can compare this sequence with the reference sequence from UniProt using a sequence alignment tool (with ClustalX for example). In case there are missing residues, you can use programs like **MODELLER** to reconstruct and model them. MODELLER provides a specific method, called Loop Optimization, for modeling loops and missing residues in PDB structures. In this proyect, you can find two example scripts to run MODELLER:

      -script_1_etapa.py > performs loop modelling (or DOPELoopModeling for higher acurracy) based on an aligmnent file you must prepare (aligmnent.ali) where the missing regions in the PDB must be defined. 
      
     -script_2_etapa.py > refines the models generated in the first step. 

    You can modify different parameters in these scripts (number of final models, structural restraints...) to suit your specific system. In the output file .log, you can evaluate the models using the DOPE score: the lower (more negative) the score, the better the model. 

-Remove non-relevant heteroatoms (water molecules, ligands, ions..).

-The structure has protons. You can add protons to your protein using tools like pdb2pqr. The protonation state must be defined according to the pH of the simulation. 

-A suitable force field must be chosen (CHARMM, AMBER, OPLS...), since it determines atom naming, protonation and topology generation in GROMACS. 

-Atoms have a compatible nomenclature with GROMACS. There are tools like pdb4all that can be used to ensure that. 
