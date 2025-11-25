from pymol import cmd

replicas = ["r1", "r2", "r3", "r4", "r5"]

def cargar_trayectorias(arg):

    # Dividir argumentos recibidos desde PyMOL
    try:
        nombre, nombre_traj = arg.split()
    except ValueError:
        print("ERROR: Debes pasar dos argumentos: nombre_base nombre_traj")
        print("Ejemplo: cargar_trayectorias bovis_FMN_2PNP bovis_FMN_2PNP")
        return

    for i in replicas:
        traj_file = f"{nombre_traj}_{i}_dt5000.xtc"
        obj_name  = f"{nombre}_{i}_fr0"
        pdb_file  = f"{nombre}_{i}_fr0.pdb"

        print(f"Cargando {pdb_file}")
        cmd.load(pdb_file, obj_name)

        print(f"Cargando trayectoria {traj_file}")
        cmd.load_traj(traj_file, obj_name)

        print(f"Alineando {obj_name}")
        cmd.intra_fit(obj_name)

# Registrar comando en PyMOL
cmd.extend("cargar_trayectorias", cargar_trayectorias)
