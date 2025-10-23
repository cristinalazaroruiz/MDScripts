import gromacs
print("*****************************************************************************************")
print("Welcome to GROMACS script for basic MD simulations with GROMACS WRAPPER framework")
print("You need to have GROMACS and GROMACS WRAPPER installed in your system to run this script")
print("******************************************************************************************")
print("")
print("First, some input files are required")

#Input files
force_field = input("Force Field name (usually amber03): ")
water = input("Water type (usually tip3p): ")
box_shape = input("Shape of solvent box (usually dodecahedron): ")
ions = input("path for ions.mdp: ")
emmdp = input("path for em.mdp: ")
top = input("path for topology file (if you don't have it, set a default name): ")

try:
    print("¿Do you start from a GRO file or a PDB file?")
    print("PDB >> press 1")
    print("GRO >> press 2")
    s = input("Write 1 or 2: ") 
    if s == "1":
        #generation of GRO and TOP
        try:
            pdb_file = input("Write initial PDB file: ")
            gromacs.pdb2gmx(f= pdb_file, o="protein.gro", p=top,
                        ff=force_field, water=water)
            print("GRO file and TOP file generated successfully\n")
            
        except Exception as e:
            print(f"Error in processing file {pdb_file}")
            print(f"Error: {e}\n")
            
        try:
            gromacs.editconf(f="protein.gro", o="boxed.gro",
                        bt= box_shape, d=1.0)
            print("Solvent box was created successfully\n")
            
        except Exception as e:
            print("Error in generating the solvent box")
            print(f"Error: {e}\n")
            
    elif s == "2":
        gro_file = input("Write initial GRO file: ")

        try:
            gromacs.editconf(f=gro_file, o="boxed.gro",
                        bt= box_shape, d=1.0)
            print("Solvent box was created successfully\n")
            
        except Exception as e:
            print("Error in generating the solvent box")
            print(f"Error: {e}\n")  
    
    else:
        print("Wrong input. Write 1 or 2. ")
            
    #Solvatation 
    try:
        gromacs.solvate(cp="boxed.gro", cs="spc216.gro", p=top,
                    o="solvated.gro")
        print("Solvatation was done successfully\n")
        
    except Exception as e:
        print("Error in solvatation")
        print(f"Error: {e}\n")
    
    #Ionization
    try:
        gromacs.grompp(f=ions, c="solvated.gro", p=top,
                o="ions.tpr")
    
        gromacs.genion.run(s="ions.tpr", p=top,pname="NA", nname="CL", 
                    neutral=True, o="ions.gro",  input=("SOL\n",))
        
        print("Ionization was done successfully\n")
        
    except Exception as e:
        print("Error in ionization")
        print(f"Error: {e}\n")
        
    #Minimization
    try:
        gromacs.grompp(f=emmdp, c="ions.gro", p=top,
                   o="em.tpr")
        
        gromacs.mdrun(v=True, s="em.tpr", deffnm= "protein_em")
        print("Minimization was done successfully\n")
        
        
    except Exception as e:
        print("Error in minimization")
        print(f"Error: {e}\n")
    
    #Index
    print("¿Do you want to create an index?")
    n = input("Write YES or NO: ").strip().upper()
    
    if n == "YES":
    
        try:
            print("****************************************************************")
            print("Index MENU")
            print("****************************************************************")
            gromacs.make_ndx(f='protein_em.gro', o='md.ndx')
            print("Index was done successfully\n")
        
        except Exception as e:
            print("Error in minimization")
            print(f"Error: {e}")
        
    elif n == "NO":
        print("MDsimulation is done")
    
    else:
        print("Unknown input. Write YES or NO. ")

except Exception as e:
    print("Something went wrong. MD simulations was not run")
    print(f"Error: {e}")

