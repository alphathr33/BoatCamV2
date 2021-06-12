#!/bin/bash

if ping -q -c 1 -W 1 google.com > /dev/null; then
    echo "The network is up"
else
    echo "The network is down"
fi

cd ~/Desktop/BoatCamV2

git reset --hard
git clean -fd
git pull https://github.com/alphathr33/BoatCamV2.git

cd Code4Display

sed -i 's/.from PyQt5 import sip/import sip' BoatCamV2.py