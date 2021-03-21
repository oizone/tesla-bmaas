#!/bin/bash

ISOPATH=/iso

for iso in `find ${ISOPATH} -type f -name "*.iso"`
do
    echo ${iso}
done
