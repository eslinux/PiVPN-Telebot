Using telegram bot to control PiVPN

Hướng dẫn cài đặt và sử dụng:
https://eslinuxprogramming.blogspot.com/2020/01/using-telegram-bot-to-control-raspberry.html

        ::: Control all PiVPN specific functions!
        :::  /addclient <client name>   Create a client ovpn profile
        :::  /delclient <client name>   Revoke a client ovpn profile
        :::  /getovpn   <client name>   Get ovpn profile of client
        :::  /listclient       			List created clients
        :::  /listconnection   			List all valid and revoked certificates
        :::  /getinfo          	        List some information: ip, dns, port, proto, ...
        ::: 
        ::: Admin management
        :::  /adduser  <username>   Add new user, who can create/del ovpn profile
        :::  /deluser  <username>   Delete user
        :::  /listuser          List all user
        :::  /listclientall     List all created clients
        :::  /logcmd  <opt>     Get log info or clear log file
        :::  /setdns <dns addr> Set dns address
        ::: 
        ::: Pi management
        :::  /reboot <yes or no>    Reboot raspberry pi server
        :::  /restartnetwork        Restart network
        :::  /runcommand <command>  Run any command and get output
        :::  /updatebot             Update PiVPN Telebot
