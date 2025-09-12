#!/bin/bash

# recordar activar entorno o instalar acpype en el sistema

for file in ready_*.mol2  # cambiar aqui por los nombres que correspondan
do
    echo "Procesando $file ..."
    
    if acpype -i "$file" -c user -a gaff -o gmx; then
        echo "✅ $file procesado correctamente."
    else
        echo "❌ Error procesando $file. Se omite y se continúa con el siguiente."
    fi

done

echo "➡️ Script terminado."

