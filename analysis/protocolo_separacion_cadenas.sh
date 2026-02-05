#!/bin/bash

states=(
Y126A_8rfn Y126A_8rfm
Y126E_8rfn Y126E_8rfm
Y126F_8rfn Y126F_8rfm
Y128A_8rfn Y128A_8rfm
Y128E_8rfn Y128E_8rfm
Y128F_8rfn Y128F_8rfm
F232A_8rfn F232A_8rfm
F232E_8rfn F232E_8rfm
F232Y_8rfn F232Y_8rfm
)


#recorrer todos los estados, todas las cadenas y todas las replicas
for state in "${states[@]}"; do
   for chain in ChainA ChainB; do
      for r in r2 r3 r4 r5; do #r1 already done

       base_state="${state%%_*}"

       dir_originalfiles="/mnt/c/Users/usuario/Desktop/clazaro_files/NQO1/mutantes/NQO1"
       dir_remoda="/mnt/c/Users/usuario/Desktop/reMoDA-GROMACS-2023-or-higher-in-development-/NQO1"

#!!!!revisar toda la nomenclatura de todos los ficheros
      ndx="${dir_originalfiles}/${state}/${base_state}-complex.ndx" #index without chain separation (not used in this case)
      ndx2="${dir_remoda}/${state}_${chain}/${base_state}-complex_chains.ndx" #index with chain separation

      xtc="${dir_originalfiles}/${state}/${r}/${base_state}_${r}_dt200.xtc" #original xtc
      xtc_cut="${dir_remoda}/${state}_${chain}/${r}/${base_state}_${r}_nopbc_${chain}.xtc" #new xtc generated from cut tpr

      tpr="${dir_originalfiles}/${state}/${r}/${base_state}_${r}.tpr" #original tpr (not used in this case)
      tpr_cut="${dir_remoda}/${state}_${chain}/${r}/${base_state}_${r}_${chain}.tpr" #tpr for chainA or chainB generated from gmx convert-tpr
      edr="${dir_originalfiles}/${state}/${r}/${base_state}_${r}.edr" #edr doesnt depend on chains

      pdb="${dir_originalfiles}/${state}/${r}/${base_state}_frame0.pdb" #original pdb (probably not needed)
      gro_cut="${dir_remoda}/${state}_${chain}/${r}/${base_state}_frame0_${chain}.gro"  #gro from each chain


#check all files exist
  if [[ ! -f "$ndx2" || ! -f "$xtc" || ! -f "$tpr" || ! -f "$edr" ]]; then
        echo "⚠ Missing input files in ${state} ${chain} ${r}. Skipping."
        continue
    fi

    echo "🔹 Processing ${state} ${chain} ${r}"

#first of all, we have to create the new directories (folders for r2, r3, r4, r5)
mkdir -p "${dir_remoda}/${state}_${chain}/${r}"

 #create ndx (probably not needed) > first we have to create pdb from frame 0 of complex xtc and then use it to create chain_index

	 # Create pdb
#    echo "Complex" | gmx trjconv -s "$tpr" -f "$xtc" -n "$ndx" -o "$pdb" || continue

    	# Create index with ChainA and ChainB
#    printf "del 0-99\nchain A\nname 0 ChainA\nchain B\nname 1 ChainB\nq\n" | \
#        gmx make_ndx -f "$pdb" -o "$ndx2" || continue
#
#now he have to create tpr_cut
	if echo "$chain" | gmx convert-tpr  -s "$tpr" -n "$ndx2" -o "$tpr_cut";then
            echo "File $tpr_cut created successfully"
else
        echo "Unable to create $tpr_cut"
        continue

fi

#then, he have to create xtc_cut from tpr_cut
#
# # Create xtc for each chain for tpr_cut
if echo "System" | gmx trjconv -f "$xtc" -s "$tpr_cut" -o "$xtc_cut"; then
            echo "$xtc_cut generated successfully"
else
        echo "Unable to create $xtc_cut"
fi

#then, we create gro from each chain
if echo "System" | gmx trjconv -f "$xtc_cut" -s "$tpr_cut" -o "$gro_cut"; then
	echo "$gro_cut created successfully"
else
	echo "Unable to create $gro_cut"
fi
#finally, we have to copy edr to dir_remoda
cp "$edr" "${dir_remoda}/${state}_${chain}/${r}/"


done
done
done

echo "Script finshed"




