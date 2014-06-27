#!/bin/bash
cp client.py /usr/bin/airclip-client
chmod +x /usr/bin/airclip-client

mkdir -p .airclip
echo "{ \"Client-ID\": \"21320\" }" > $HOME/.airclip/client.conf

apt-get -y install xbindkeys
xbindkeys --defaults > ~/.xbindkeysrc

echo \"airclip-client copy\" >> ~/.xbindkeysrc 
echo "   Control+Alt + c" >> ~/.xbindkeysrc 

echo \"airclip-client paste\" >> ~/.xbindkeysrc 
echo "   Control+Alt + v" >> ~/.xbindkeysrc 

echo \"airclip-client append\" >> ~/.xbindkeysrc 
echo "   Control+Alt + a" >> ~/.xbindkeysrc 

killall xbindkeys && xbindkeys

