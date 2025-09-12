#!/bin/bash

for file in *.mol2
do
    base_name="${file%.pdb}"

    # 1. Generar archivo temporal con obabel
    obabel -imol2 "$file" -ocom -O "${base_name}_temp.com"

    # 2. Tomar solo las coordenadas, omitiendo la cabecera automática
    tail -n +7 "${base_name}_temp.com" > "${base_name}_coords.com"

    # 3. Crear el .com final con nuestra cabecera personalizada
    {
        echo "#p opt hf/6-31G* pop=mk iop(6/33=2,6/42=6)"
        echo
        echo "$base_name"
        echo
        echo "-2  1"
        cat "${base_name}_coords.com"
    } > "${base_name}.com"

    # 4. Borrar archivos temporales
    rm "${base_name}_temp.com" "${base_name}_coords.com"
done



