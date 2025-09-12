#!/bin/bash

for file in *.log
do
    base_name="${file%.log}"

    # 1. Generar archivo mol2 con obabel
    obabel -ilog "$file" -omol2 -O "${base_name}.mol2"
done


