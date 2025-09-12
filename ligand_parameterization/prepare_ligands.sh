#!/bin/bash

# Script to convert all .mol2 to GAUSSIAN input (.com files)
# Remember to activate the conda environment or install OPENBABEL (obabel) on your system
# Change Gaussian header if necessary (charges and multiplicity will probably need changes)

# Process all .mol2 files
for file in *.mol2
do
    base_name="${file%.mol2}"
    echo ""
    echo "Processing $file ..."

    # 1. Produce temporary file with obabel (skip file if it fails)
    if ! obabel -imol2 "$file" -ocom -O "${base_name}_temp.com"; then
        echo "❌ Failed to convert $file, skipping..."
        continue  # skip to next file
    fi

    # 2. Take only coordinate information, omitting default header
    tail -n +7 "${base_name}_temp.com" > "${base_name}_coords.com"

    # 3. Create final .com with customized header
    {
        echo "#p opt hf/6-31G* pop=mk iop(6/33=2,6/42=6)"
        echo
        echo "$base_name"
        echo
        echo "-2  1"
        cat "${base_name}_coords.com"
    } > "${base_name}.com"

    # 4. Delete temporary files
    rm "${base_name}_temp.com" "${base_name}_coords.com"
    echo "$file converted successfully to ${base_name}.com"
done

echo "All files processed."
