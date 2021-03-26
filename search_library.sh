#!/bin/bash
IFS=:

for p in ${LD_LIBRARY_PATH}; do
    if [ -e ${p}/${1} ]; then
        echo ${p}
    fi
done