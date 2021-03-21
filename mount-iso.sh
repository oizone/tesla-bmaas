#!/bin/bash

ISOPATH="/iso"
MOUNTBASE="/httpboot/iso/"

for iso in `find ${ISOPATH} -type f -name "*.iso"`
do
    ISONAME=`echo ${iso}|cut -d"/" -f 3`
    mkdir "${MOUNTBASE}${ISONAME}"
    mount -o loop ${iso} "${MOUNTBASE}${ISONAME}"
done
