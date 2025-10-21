#!/bin/bash
# Interactive script to run CPPTRAJ and calculate distance and correlation matrix (in DAT and en NPY)

# === 1. Read al files ===
read -p "Topology (.prmtop): " TOPO
read -p "Reference (.pdb): " REF
read -p "Trayectory (.xtc/.nc): " TRAJ
read -p "Name of distance matrix (.dat): " DIST
read -p "Name of correlation matrix (.dat): " CORR
read -p "Name of log file (.log): " LOG
# === 2. Show settings===
echo ""
echo "   Run CPPTRAJ with:"
echo "   Topology     : $TOPO"
echo "   Reference    : $REF"
echo "   Trayectory   : $TRAJ"
echo "   Distance     :  $DIST"
echo "   Correlation  : $CORR"
echo ""

# === 3.Run CPPTRAJ managing exceptions ===
if cpptraj <<EOF > $LOG
parm $TOPO
reference $REF
trajin $TRAJ 1 last 1

# If there are solvent or ions
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
    echo "CPPTRAJ finshed successfully."
    echo "Log saved in: $LOG"

    #== 5. Change .dat to .npy with Python (numpy) ==
    python - <<END
import numpy as np
try:
	# Load matrix from .DAT
	dist = np.loadtxt("$DIST")
	corr = np.loadtxt("$CORR")
	print("First lines of distance matrix: ")
	print(f"{dist[:5, :]}")

	print("\nfirst lines of corr matrix: ")
	print(f"{corr[:5, :]}")
	
	#Save as float32 in .NPY format
	np.save("${DIST%.dat}.npy", dist.astype(np.float32))
	np.save("${CORR%.dat}.npy", corr.astype(np.float32))

	print("Files converted to .NPY: ${DIST%.dat}.npy, ${CORR%.dat}.npy")

except Exception as e:
	print("Error when converting DAT to NPY with Python (numpy")
	print(f"Error details: {e}")
END

else
    # === 5. Error message if CPPTRAJ fails ===
    echo ""
    echo "Error in CPPTRAJ. $LOG"
fi

echo ""
echo "End of script"

