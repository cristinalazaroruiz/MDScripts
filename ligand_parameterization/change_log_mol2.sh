#!/bin/bash

# Script to transform Gaussian coordinate output (.log) to mol2
# Remember to activate the conda environment or install OPENBABEL (obabel) on your system

for file in *.log
do
    base_name="${file%.log}"
    echo ""
    echo "Processing $file ..."

    # Try to convert with obabel, skip file if it fails
    if ! obabel -ilog "$file" -omol2 -O "${base_name}.mol2"; then
        echo "❌ Failed to convert $file, skipping..."
        continue  # skip to next file
    fi

    echo "✅ $file converted successfully to ${base_name}.mol2"
done

echo "All files processed."
