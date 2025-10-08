#!/bin/bash

# Script to transform mol2 to pdb
# Remember to activate the conda environment or install OPENBABEL (obabel) on your system

for file in *.mol2
do
    base_name="${file%.mol2}"
    echo ""
    echo "Processing $file ..."

    # Try to convert with obabel, skip file if it fails
    if ! obabel -imol2 "$file" -opdb -O "${base_name}.pdb"; then
        echo "❌ Failed to convert $file, skipping..."
        continue  # skip to next file
    fi

    echo "✅ $file converted successfully to ${base_name}.pdb"
done

echo "All files processed."