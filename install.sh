#!/bin/bash

_currdir="$(pwd)"

pivpn_path="$(which pivpn)"
if [ -z "$pivpn_path" ]
then
      echo "pivpn have not installed yet, please install pivpn first !!!"
      exit 1
fi

#setup your TelegramBot token
echo -e "\n"
echo "what is your telegram bot token: "
read bot_token
if [ -z "$bot_token" ]
then
      echo "please input your telegram bot token"
      exit 1
fi

echo "Save telegram bot token to $HOME/ovpns/telebot.token"
echo "$bot_token" > "$HOME/ovpns/telebot.token"

#setup your telegram account info
echo -e "\n"
echo "What is your telegram username (without space, from [a-z] and [0-9]): "
read tele_username
if [ -z "$tele_username" ]
then
      echo "please input your telegram username"
      exit 1
fi

echo -e "\n"
echo "What is your telegram chatid (without space, [0-9]): "
read tele_chatid
if [ -z "$tele_chatid" ]
then
      echo "please input your telegram chatid"
      exit 1
fi

cur_date="$(date '+%Y-%m-%d')"
tele_type="admin"

echo -e "\n"
echo "Save telegram account info to $HOME/ovpns/userlist.txt"
echo "[username]" 											 > "$HOME/ovpns/userlist.txt"
echo "IDNUM USERNAME CHATID TYPE TIME" 						>> "$HOME/ovpns/userlist.txt"
echo "1 $tele_username $tele_chatid $tele_type $cur_date"   >> "$HOME/ovpns/userlist.txt"
cat "$HOME/ovpns/userlist.txt"

#install app
echo -e "\n"
echo "Installing application ..."
sudo cp -rf "$_currdir/pivpntelebot.py" "/usr/bin"
sudo cp -rf "$_currdir/pivpntelebot.sh" "/usr/bin"
sudo chmod +x /usr/bin/pivpntelebot.py
sudo chmod +x /usr/bin/pivpntelebot.sh
sudo cp -rf "$_currdir/pivpntelebot.service" "/lib/systemd/system"
sudo chmod 644 /lib/systemd/system/pivpntelebot.service


echo "Start pivpntelebot service ..."
#sudo systemctl start pivpntelebot
#sudo systemctl status pivpntelebot
#sudo systemctl stop pivpntelebot
sudo systemctl restart pivpntelebot
sudo systemctl enable pivpntelebot
#sudo systemctl disable pivpntelebot
echo "Setup finished !"

exit 0
