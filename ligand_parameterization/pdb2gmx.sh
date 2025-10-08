#!/bin/bash

# Script to transform ligands in pdb format to gmx
# Remember to activate the conda environment or install GROMACS (gmx editconf) on your system

for file in *.pdb
do
    base_name="${file%.pdb}"
    echo ""
    echo "Processing $file ..."

    # Try to convert, skip file if it fails
    if ! gmx editconf -f "$file" -o "$base_name.gro"; then
        echo "❌ Failed to convert $file, skipping..."
        continue  # skip to next file
    fi

    echo "✅ $file converted successfully to $base_name.gro"
done

echo "All files processed."
