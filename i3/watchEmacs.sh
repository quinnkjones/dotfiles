#!/usr/bin/zsh
while [[ ! -e /tmp/emacs1000/server ]]
do
    sleep 5
done
notify-send "emacs loaded"

