#!/bin/bash
sudo cp client.py /usr/bin/airclip-client
sudo chmod +x /usr/bin/airclip-client

mkdir -p $HOME/.airclip
echo "{" > $HOME/.airclip/client.conf
echo " \"Client-ID\": \"21320\", " >> $HOME/.airclip/client.conf
echo " \"Server-URL\": \"http://127.0.0.1:80/airclip\" " >> $HOME/.airclip/client.conf
echo "}" >> $HOME/.airclip/client.conf

sudo apt-get -y install xbindkeys xsel xclip
sudo pip install pyperclip
xbindkeys --defaults > ~/.xbindkeysrc

echo \"airclip-client copy\" >> ~/.xbindkeysrc 
echo "   Control+Alt + c" >> ~/.xbindkeysrc 

echo \"airclip-client paste\" >> ~/.xbindkeysrc 
echo "   Control+Alt + v" >> ~/.xbindkeysrc 

echo \"airclip-client append\" >> ~/.xbindkeysrc 
echo "   Control+Alt + a" >> ~/.xbindkeysrc 

killall xbindkeys && xbindkeys

