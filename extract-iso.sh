#!/bin/bash

ISOPATH="/iso"
MOUNTBASE="/httpboot/iso/"

for iso in `find ${ISOPATH} -type f -name "*.iso"`
do
    ISONAME=`echo ${iso}|cut -d"/" -f 3|cut -d"." -f 1`
    mkdir -p "${MOUNTBASE}${ISONAME}"
    7z x -y -o"${MOUNTBASE}${ISONAME}" ${iso}
done
