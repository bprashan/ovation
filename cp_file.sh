#!/bin/bash

mkdir patch
find . -type f -name "*.bak" | while read -r bak_file; do
    # Copy the .bak file to the patch directory
    cp "$bak_file" patch
    echo "$bak_file"
    # Determine the relevant file path by removing the .bak extension
    relevant_file="${bak_file%.bak}"
    # Check if the relevant file exists and copy it to the patch directory
    if [ -f "$relevant_file" ]; then
        cp "$relevant_file" patch
    fi
done
