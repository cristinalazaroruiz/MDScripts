#!/bin/bash

# Script to add a force field to ligands with ANTECHAMBER (via ACPYPE)
# Remember to activate the conda environment or install ACPYPE on your system
# Change ACPYPE parameters if necessary

for file in ready_*.mol2  # change file pattern name if necessary
do
    echo "Processing $file ..."
    
    if acpype -i "$file" -c user -a gaff -o gmx; then
        echo "✅ $file processed successfully."
    else
        echo "❌ Error in $file. This file will be skipped, and the next one will be processed."
    fi
done

echo "➡️ Script finished."
