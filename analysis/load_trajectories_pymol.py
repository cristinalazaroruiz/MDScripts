from pymol import cmd

base_name = "F232Y"
replicas = ["r1", "r2", "r3", "r4", "r5"]
states = [f"{base_name}_8rfm", f"{base_name}_8rfn"]

for state in states:
    for r in replicas:
        folder = f"{state}/{r}"
        xtc = f"{folder}/{base_name}_{r}_nopbc.xtc"
        gro = f"{folder}/frame0_{r}.gro"
        obj = f"{state}_{base_name}_{r}"

        cmd.load(gro, obj)
        cmd.load_traj(xtc, obj, interval=100)
 
