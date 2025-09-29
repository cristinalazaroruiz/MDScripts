# Loop refinement of an existing model
from modeller import *
from modeller.automodel import *

#from modeller import soap_loop
log.verbose()
env = Environ()

# directories for input atom files
env.io.atom_files_directory = ["."]

# Create a new class based on ’LoopModel’ so that we can redefine
# select_loop_atoms (necessary)
class MyLoop(LoopModel):
# This routine picks the residues to be refined by loop modeling
    def select_loop_atoms(self):
# Choose residues to refine
        return Selection(self.residue_range("1:A", "48:A"))
# Two loops simultaneously
#return Selection(self.residue_range(’19:A’, ’28:A’),
# self.residue_range(’38:A’, ’42:A’))

m = MyLoop(env,
           inimodel="Q9NVS9.BL00020002.pdb", # initial model of the target
           sequence="1NRG", # code of the target
           loop_assess_methods=assess.DOPE) # assess loops with DOPE
# loop_assess_methods=soap_loop.Scorer()) # assess with SOAP-Loop


m.loop.starting_model= 5 # index of the first loop model
m.loop.ending_model = 7 # index of the last loop model
m.loop.md_level = refine.slow # loop refinement method
m.make()

