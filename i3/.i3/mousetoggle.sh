#!/bin/bash

declare -i ID
ID=`xinput list | grep -Eo 'DLL063E:00 06CB:2934\s*id\=[0-9]{1,2}' | grep -Eo '[0-9]{1,2}' | tail -1`
declare -i STATE
STATE=`xinput list-props $ID|grep 'Device Enabled'|awk '{print $4}'`
if [ $STATE -eq 1 ]
then
    xinput disable $ID
    echo "Touchpad disabled."
else
    xinput enable $ID
    echo "Touchpad enabled."
fi
