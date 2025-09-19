# PROTEIN PREPARATION

Within MD Simulations, a very important step is the preparation of the protein 3D structure. We have to make sure that:

-There are not missing residues (especially if the structure has been obtained experimentally, like crystallography). To do so, you can use script residue_check.py to extract PDB sequence. Afterwards, you can compare this sequence with the one present in UniProt using a sequence alignment (with ClustalX for example).

-Remove non-relevant heteroatoms (water molecules, ligands, ions..).

-The structure has protons. You can add protons to your protein using tools like pdb2pqr. The protonation state must be defined according to the pH of the simulation. 

-A suitable force field must be chosen (CHARMM, AMBER, OPLS...), since it determines atom naming, protonation and topology generation in GROMACS. 

-Atoms have a compatible nomenclature with GROMACS. There are tools like pdb4all that can be used to ensure that. 
