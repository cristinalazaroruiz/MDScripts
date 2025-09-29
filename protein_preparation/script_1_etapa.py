#Import all libraries from modeller
from modeller import *
from modeller.automodel import *  # Load the AutoModel / LoopModel class / DOPE-based loop modeling
#AutoModel > basic modelling
#LoopModel > modelling loops and missing parts in the PDB structure
#DOPELoopModel > like LoopModel but more exhaustive

log.verbose()

#If we want to add new characteristics, we have to create a new class (MyModel)
#This new class inherits methods from the original class (AutoMOdel, LoopModel etc)

class MyModel(DOPELoopModel):
#    def special_restraints(self, aln):
#        # Constrain the A and B chains to be identical (C-alpha only)
#        s1 = Selection(self.chains['A']).only_atom_types('CA')
#        s2 = Selection(self.chains['B']).only_atom_types('CA')
#        self.restraints.symmetry.append(Symmetry(s1, s2, 1.0))

#    def user_after_single_model(self):
#        # Report on symmetry violations greater than 1A
#        self.restraints.symmetry.report(1.0)

    #model only some specific residues
    def select_loop_atoms(self):
        return Selection(self.residue_range("1:A", "48:A"),
                        self.residue_range("262:B", "309:B"))


env = Environ()
env.io.atom_files_directory = ['.']  # directory with PDB files


#use MyModel or the class that we want in the prediction
a = MyModel(env,
            alnfile='alignment.ali',  # alignment filename
            knowns='1NRG',            # template
            sequence='Q9NVS9',        #sequence
            loop_assess_methods=assess.DOPE) #generate score for each structure

#DOPE> the smaller (more negative) the best

a.starting_model = 1
a.ending_model = 3 #how many models we want to generate
a.loop.starting_model = 1
a.loop.ending_model = 2 #how many refinement
a.loop.md_level = refine.slow #refinement more exhaustive

#build the models
a.make()  
