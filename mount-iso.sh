#!/bin/bash

ISOPATH="/iso"

for iso in `find ${ISOPATH} -type f -name "*.iso"`
do
    MOUNTNAME=`echo ${iso}|cut -d"." -f 1`
    mkdir ${MOUNTNAME}
    mount -o loop ${iso} ${MOUNTNAME}
done
