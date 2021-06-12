#!/bin/bash

if ping -q -c 1 -W 1 google.com > /dev/null; then
    echo "The network is up"
else
    echo "The network is down"
fi

ps -ef | grep "BoatCamV2.py" | awk '{print $2}' | xargs sudo kill

cd ~/Desktop/BoatCamV2

git reset --hard
git clean -fd
git pull https://github.com/alphathr33/BoatCamV2.git

cd Code4Display
chmod a+x update.sh
sed -i 's/from PyQt5 import sip/import sip/' BoatCamV2.py

python3 BoatCamV2.py
