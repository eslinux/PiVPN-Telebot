#!/bin/bash

telebot_tmp="/tmp/PiVPNTelebot"
telebot_filename="PiVPN-Telebot-master"

echo "Create $telebot_tmp ..."
rm -rf "$telebot_tmp"
mkdir "$telebot_tmp"
cd "$telebot_tmp"


echo "Donwloading ..."
wget --no-check-certificate --content-disposition https://github.com/eslinux/PiVPN-Telebot/archive/master.zip &> /dev/null
if test -f "$telebot_filename.zip"; then
    echo "$telebot_filename.zip downloaded"
else
	echo "$telebot_filename.zip download faild"
	exit 1
fi


echo "Unzip ..."
unzip "$telebot_filename.zip" &> /dev/null
if [ ! -d "$telebot_filename" ]
then
    echo "unzip $telebot_filename.zip failed !!!" 
    exit 1
fi


echo "Installing ..."
cd "$telebot_filename"
sudo cp -rf "pivpntelebot.py" "/usr/bin"
sudo cp -rf "pivpntelebot.sh" "/usr/bin"
sudo cp -rf "pivpntelebotupdate.sh" "/usr/bin"
sudo chmod +x /usr/bin/pivpntelebot.py
sudo chmod +x /usr/bin/pivpntelebot.sh
sudo chmod +x /usr/bin/pivpntelebotupdate.sh

exit 0
