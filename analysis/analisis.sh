#!/bin/bash
# Script interactivo para ejecutar CPPTRAJ y calcular matrices de distancia y correlación (en dat y en npy)

# === 1. Leer los nombres de los ficheros ===
read -p "Topología (.prmtop): " TOPO
read -p "Referencia (.pdb): " REF
read -p "Trayectoria (.xtc/.nc): " TRAJ
read -p "Nombre matriz de distancias (.dat): " DIST
read -p "Nombre matriz de correlaciones (.dat): " CORR
read -p "Nombre del fichero log (.log): " LOG
# === 2. Mostrar configuración ===
echo ""
echo "   Ejecutando CPPTRAJ con:"
echo "   Topología     : $TOPO"
echo "   Referencia    : $REF"
echo "   Trayectoria   : $TRAJ"
echo "   Distancias →  $DIST"
echo "   Correlación → $CORR"
echo ""

# === 3. Ejecutar CPPTRAJ con control de errores ===
if cpptraj <<EOF > $LOG
parm $TOPO
reference $REF
trajin $TRAJ 1 last 1

# Si hay solvente o iones:
# parmstrip :SOL,:NA,:CL
# strip :SOL
# strip :NA,:CL

autoimage
center :1-9999 mass origin
rms reference @CA
matrix dist @CA out $DIST
matrix correl @CA out $CORR
run
exit
EOF
then
    # === 4. Finalizar si todo va bien ===
    echo ""
    echo "✅ CPPTRAJ finalizado correctamente."
    echo "Log guardado en: $LOG"

    #== 5. Convertir .dat a .npy usando Python ==
    python - <<END
import numpy as np
try:
	#Cargar matrices desde .dat
	dist = np.loadtxt("$DIST")
	corr = np.loadtxt("$CORR")
	print("First lines of distance matrix: ")
	print(f"{dist[:5, :]}")

	print("\nfirst lines of corr matrix: ")
	print(f"{corr[:5, :]}")
	
	#Guardar como float32 en formato .npy
	np.save("${DIST%.dat}.npy", dist.astype(np.float32))
	np.save("${CORR%.dat}.npy", corr.astype(np.float32))

	print("✅ Archivos convertidos a .npy: ${DIST%.dat}.npy, ${CORR%.dat}.npy")

except Exception as e:
	print("Error al convertir los ficheros .dat a .npy con Python (numpy)")
	print(f"Detalles del error: {e}")
END

else
    # === 5. Mensaje de error si CPPTRAJ falla ===
    echo ""
    echo "❌ Error: CPPTRAJ terminó con errores. $LOG"
fi

echo ""
echo "Fin del script"

