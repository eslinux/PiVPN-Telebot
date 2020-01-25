import sys
import time
import random
import datetime
import telepot
import shlex
import subprocess
import os
import re


def getVpnDev():
    cmd = shlex.split("/bin/bash -c \"cat /etc/openvpn/server.conf | grep -w \"dev\"\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    vpn_dev = ""
    if (pivpn.returncode == 0):
        line = pivpn.stdout.readline().strip()
        linearr = line.split(" ")
        vpn_dev = linearr[1]
    return vpn_dev.strip()


def getVpnProto():
    cmd = shlex.split("/bin/bash -c \"cat /etc/openvpn/server.conf | grep -w \"proto\"\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    vpn_proto = ""
    if (pivpn.returncode == 0):
        line = pivpn.stdout.readline().strip()
        linearr = line.split(" ")
        vpn_proto = linearr[1]
    return vpn_proto.strip()


def getVpnPort():
    cmd = shlex.split("/bin/bash -c \"cat /etc/openvpn/server.conf | grep -w \"port\"\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    vpn_port = ""
    if (pivpn.returncode == 0):
        line = pivpn.stdout.readline().strip()
        linearr = line.split(" ")
        vpn_port = linearr[1]
    return vpn_port.strip()


def getVpnIp():
    cmd = shlex.split("/bin/bash -c \"ifconfig " + getVpnDev() + "0 | grep \"netmask\"\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    pi_ip = ""
    pi_netmask = ""
    if (pivpn.returncode == 0):
        line = pivpn.stdout.readline().strip()
        linearr = line.split(" ")
        couter = 0
        for item_t in linearr:
            if (item_t == "inet"):
                pi_ip = linearr[couter + 1]
            elif (item_t == "netmask"):
                pi_netmask = linearr[couter + 1]
            couter = couter + 1
    return (pi_ip + " / " + pi_netmask).strip()


def getPiIp():
    cmd = shlex.split("/bin/bash -c \"ifconfig | grep \"netmask\"\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    pi_ip = ""
    pi_netmask = ""
    vpn_ip_arr = getVpnIp().split()
    vpn_ip = vpn_ip_arr[0]
    if (pivpn.returncode == 0):
        for line in pivpn.stdout:
            line = line.strip()
            if not ((line.find(vpn_ip) != -1) or (line.find("127.0.0.1") != -1)):
                linearr = line.split()
                pi_ip = linearr[1].strip()
                pi_netmask = linearr[3].strip()
                break

    return (pi_ip + " / " + pi_netmask)


def getDns():
    cmd = shlex.split("/bin/bash -c \"sudo cat /etc/openvpn/easy-rsa/pki/Default.txt | grep \"remote\"\"")
    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
    pivpn.wait()
    vpn_dns = ""
    if (pivpn.returncode == 0):
        line = pivpn.stdout.readline().strip()
        linearr = line.split(" ")
        vpn_dns = linearr[1]

    return vpn_dns.strip()

def setDns(chatid, ndns):
    odns = getDns()
    if odns == "":
        return "Can not get current dns address setting !!!"

    if not checkSyntax(ndns):
        return "Dns address syntax error !!!"

    if ndns == ndns:
        return "New dns address is the same with current dns address !!!"

    sedcmd = "sudo sed -i 's/" + odns + "/" + ndns + "/g' /etc/openvpn/easy-rsa/pki/Default.txt"
    cmd = shlex.split("/bin/bash -c \"" + sedcmd + "\"")
    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  universal_newlines=True)
    pivpn.wait()

    retmsg = ndns + ": Set ok !"
    if not (pivpn.returncode == 0):
        retmsg = ndns + ": Set failed !"

    return retmsg



def reboot(chatid):
    if checkUserType(chatid) != "admin":
        return "Permission denied, you can not reboot !"
    bot.sendMessage(chatid, "Rebooting ...")
    time.sleep(3)

    cmd = shlex.split("/bin/bash -c \"sudo reboot\"")
    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    return "rebotting ...."

def restartNetwork(chatid):
    if checkUserType(chatid) != "admin":
        return "Permission denied, you can not restart network !"

    bot.sendMessage(chatid, "Restarting network ...")
    time.sleep(3)

    cmd = shlex.split("/bin/bash -c \"sudo service networking restart\"")
    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    time.sleep(10)
    return "Restarted network !!!"


def logCmd(chatid, cmd):
    logpath = WORKING_FOLDER + "log.txt"
    if not os.path.isfile(logpath):
        return "log file not exist !!!"

    retmsg = "Command fail !!!"
    if cmd == "1":
        flog = open(logpath, "rb")
        time.sleep(3)
        bot.sendDocument(chatid, flog)
        time.sleep(3)
        flog.close()
        retmsg = "Sent log file"
    elif cmd == "2":
        timets = time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())
        logpath_bak = WORKING_FOLDER + timets + "_log.txt"

        cmd = shlex.split("/bin/bash -c \"cp -rf "+logpath+ " " +logpath_bak+ "\"")
        pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        pivpn.wait()
        time.sleep(3)
        cmd = shlex.split("/bin/bash -c \"echo " + timets + " Created new log file > " + logpath + "\"")
        pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        pivpn.wait()
        retmsg = "Backup log file: " + logpath_bak

    return retmsg


def getHelp(chatid):
    retmsg = "You can not use this Bot !!!"

    usertype = checkUserType(chatid)
    if usertype == "admin":
        retmsg = " \
        ::: Control all PiVPN specific functions! \n \
        :::  /addclient <client name>   Create a client ovpn profile \n \
        :::  /delclient <client name>   Revoke a client ovpn profile \n \
        :::  /getovpn   <client name>   Get ovpn profile of client \n \
        :::  /listclient       			List created clients \n \
        :::  /listconnection   			List all valid and revoked certificates \n \
        :::  /getinfo          	        List some information: ip, dns, port, proto, ... \n \
        ::: \n \
        ::: \n \
        ::: Admin management \n \
        :::  /adduser  <username>   Add new user, who can create/del ovpn profile \n \
        :::  /deluser  <username>   Delete user \n \
        :::  /listuser          List all user \n \
        :::  /listclientall     List all created clients \n \
        :::  /logcmd  <opt>     Get log info or clear log file \n \
        :::  /setdns <dns addr> Set dns address \n \
        ::: \n \
        ::: \n \
        ::: Pi management \n \
        :::  /reboot <yes or no>    Reboot raspberry pi server\n \
        :::  /restartnetwork        Restart network\n \
        :::  /runcommand <command>  Run any command and get output \n \
        "

    elif usertype == "normal":
        retmsg = " \
        ::: Control all PiVPN specific functions! \n \
        :::  /addclient <client name>   Create a client ovpn profile \n \
        :::  /delclient <client name>   Revoke a client ovpn profile \n \
        :::  /getovpn   <client name>   Get ovpn profile of client \n \
        :::  /listclient       			List created clients to the server \n \
        :::  /listconnection   			List all valid and revoked certificates \n \
        :::  /getinfo          		List some information: ip, dns, port, proto, ... \n \
        "
    return retmsg





def pivpnListClient(chatid):
    retmsg = "You have not created any client yet !!!"
    fpath = WORKING_FOLDER + str(chatid) + ".txt"
    if os.path.isfile(fpath):
        seting_f = open(fpath, "r")
        list = seting_f.readlines()
        seting_f.close()
        if len(list) > 0:
            retmsg = ""
            for line in list:
                retmsg = retmsg + line
    return retmsg


def pivpnListClientAll(chatid):
    retmsg = str()
    counter = 0
    if checkUserType(chatid) == "admin":
        cmd = shlex.split("/bin/bash -c \"ls -l /home/pi/ovpns\"")
        pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        pivpn.wait()
        pivpn.stdout.readline()

        for line in pivpn.stdout:
            if line.find(".ovpn") != -1:
                retmsg = retmsg + line
                counter = counter+1
    else:
        return "Permission denied, you can not list all client list !!!"

    if counter == 0:
        retmsg = "You can not list all client list !!!"

    return retmsg


def pivpnListConnection():
    cmd = shlex.split("/bin/bash -c \"pivpn -c\"")
    pivpn = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.wait()
    for num in range(0, 7):
        pivpn.stdout.readline()

    retmsg = ""
    for line in pivpn.stdout:
        retmsg = retmsg + line
    return retmsg


def pivpnAddClient(chatid, name):
    if not checkSyntax(name):
        return "Invalid client name !"

    ret = "Notthing to do !!!"
    cmd = shlex.split("/bin/bash -c \"pivpn add nopass\"")
    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pivpn.stdin.write(name + '\n')
    pivpn.stdin.flush()
    pivpn.stdin.write('1080\n')
    pivpn.stdin.flush()
    pivpn.stdin.close()
    pivpn.wait()
    for line in pivpn.stdout:
        line = line.lower()
        if line.find("successfully created") != -1:
            ts = time.gmtime()
            logmsg = time.strftime("%Y-%m-%d-%H:%M:%S", ts) + " " + name
            fpath = WORKING_FOLDER + str(chatid) + ".txt"
            os.system("echo " + logmsg + " >> " + fpath)
            ret = name + ": successfully created"
            break
        elif line.find("this name is already in use") != -1:
            ret = name + ": this name is already in use, please choose another name !!!"
            break
    return ret


def pivpnDelClient(chatid, name):
    if not checkSyntax(name):
        return "Invalid client name !"

    retmsg = name + ": not found !!!"
    fpath = WORKING_FOLDER + str(chatid) + ".txt"
    if os.path.isfile(fpath):
        seting_f = open(fpath, "r")
        clientlist = seting_f.readlines()
        seting_f.close()

        for client in clientlist:
            clientarr = client.split()
            if len(clientarr) > 1:
                if clientarr[1] == name:
                    cmd = shlex.split("/bin/bash -c \"pivpn -r\"")
                    pivpn = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    pivpn.stdin.write(name + '\n')
                    pivpn.stdin.flush()
                    pivpn.stdin.close()
                    pivpn.wait()
                    for line in pivpn.stdout:
                        line = line.lower()
                        if line.find("completed") != -1:
                            seting_f = open(fpath, "w")
                            for citem in clientlist:
                                if not (citem.find(name) != -1):
                                    seting_f.write(citem)
                            seting_f.close()
                            retmsg = name + ": deleted !!!"
                            break
                        elif line.find("valid cert name") != -1:
                            retmsg = name + ": not found !!!"
                            break


    else:
        retmsg = "You have not created any client yet !!!"

    return retmsg

def getOvpn(chatid, name):
    if not checkSyntax(name):
        return "Invalid client name !"

    retmsg = name + ": not found !!!"
    fpath = WORKING_FOLDER + str(chatid) + ".txt"
    if os.path.isfile(fpath):
        seting_f = open(fpath, "r")
        clientlist = seting_f.readlines()
        seting_f.close()

        for client in clientlist:
            clientarr = client.split()
            if len(clientarr) > 1:
                if clientarr[1] == name:
                    ovpndpath = WORKING_FOLDER + name + ".ovpn"
                    if os.path.isfile(ovpndpath):
                        fovpn = open(ovpndpath, "rb")
                        retmsg = "send " + name + ".ovpn"
                        bot.sendDocument(chatid, fovpn)
                        fovpn.close()
                        break
    return retmsg

def getInfo(chatid):
    retmsg = "List info: \n"

    retmsg = retmsg \
             + "---PiVPN---\n" \
             + "ip: " + getVpnIp()  + "\n" \
             + "port: " + getVpnPort() + "\n" \
             + "proto: " + getVpnProto() + "\n" \
             + "dns: " + getDns() + "\n" \
             + "\n" \
             + "---Pi info---\n" \
             + "ip: " + getPiIp() + "\n"

    return retmsg




def addUser(chatid, name, id, type):
    if not checkSyntax(name):
        return "Username syntax error !!!"
    if not checkSyntax(id):
        return "chatid syntax error !!!"
    if (not checkSyntax(type)) or ((type != "admin") and (type != "normal")):
        return "type syntax error, admmin/normal only !!!"

    if not (checkUserType(chatid) == "admin"):
        return "Permission denied, you can not add username !!!"

    retmsg = str(id) + ": can not add !!!"
    is_exist = False
    for useritem in user_list:
        if str(id) == str(useritem.id):
            retmsg = str(id) + " is already in use !!!"
            is_exist = True
            break
    if not is_exist:
        ts = time.gmtime()
        timestamp = time.strftime("%Y-%m-%d", ts)
        myuser = piuser(name, str(id), type, timestamp) #USERNAME CHATID TYPE TIME
        user_list.append(myuser)

        fpath = WORKING_FOLDER + "userlist.txt"
        if os.path.isfile(fpath):
            seting_f = open(fpath, "w")

            IDNUM = 0
            seting_f.write("[username]\n")
            seting_f.write("IDNUM CHATID TYPE TIME\n")
            for useritem in user_list:
                IDNUM = IDNUM + 1
                seting_f.write(str(IDNUM) + " " + useritem.username + " " + useritem.id + " " + useritem.type + " " + useritem.time + "\n")
                seting_f.flush()
            seting_f.close()
            retmsg = str(id) + ": added !!!"
    return  retmsg



def delUser(chatid, id):
    if not checkSyntax(id):
        return "id syntax error !!!"
    if not (checkUserType(chatid) == "admin"):
        return "Permission denied, you can not delete username !!!"
    if str(chatid) == str(id):
        return "you can not delete admin (your self) !!!"

    retmsg = str(id) + ": can not delete !!!"
    is_exist = False
    couter = 0
    for useritem in user_list:
        if str(id) == str(useritem.id):
            is_exist = True
            user_list.pop(couter)
            break
        couter = couter + 1

    if not is_exist:
        retmsg = str(id) + ": have not exist yet !!!"
    else:
        fpath = WORKING_FOLDER + "userlist.txt"
        if os.path.isfile(fpath):
            seting_f = open(fpath, "w")

            IDNUM = 0
            seting_f.write("[username]\n")
            seting_f.write("IDNUM USERNAME CHATID TYPE TIME\n")
            for useritem in user_list:
                IDNUM = IDNUM + 1
                seting_f.write(str(IDNUM) + " " + useritem.username + " " + useritem.id + " " + useritem.type + " " + useritem.time + "\n")
                seting_f.flush()
            seting_f.close()
            retmsg = str(id) + ": deleted !!!"
    return retmsg

def listUser(chatid):
    retmsg = "Empty !!!"

    if not (checkUserType(chatid) == "admin"):
        return "Permission denied, you can not do this command !!!"

    if len(user_list) > 0:
        retmsg = ""
        IDNUM = 0
        for useritem in user_list:
            IDNUM = IDNUM + 1
            struser = str(IDNUM) + " " + useritem.username + " " + useritem.id + " " + useritem.type + " " + useritem.time
            retmsg = retmsg + struser + "\n"
    return retmsg

class piuser:
    def __init__(self, username, id, type, time):
        self.username = username #can change
        self.id = id #can not change
        self.type = type
        self.time = time


def getTelebotToken():
    global TELEBOT_TOKEN
    TELEBOT_TOKEN=str()
    is_getok = False
    fpath = WORKING_FOLDER + "telebot.token"
    if os.path.isfile(fpath):
        seting_f = open(fpath, "r")
        tokenl = seting_f.readlines()
        seting_f.close()
        if len(tokenl):
            for tk in tokenl:
                tk = tk.strip()
                if tk != "":
                    TELEBOT_TOKEN = tk
                    is_getok = True
                    break
    return is_getok


def getUserlistInit():
    # [username]
    # IDNUM USERNAME CHATID TYPE TIME
    # 1 ninhld 1567743215 admin 2020-01-19
    # 2 maria 1014441789 normal 2020-01-30

    global user_list

    counter = 0
    fpath = WORKING_FOLDER + "userlist.txt"
    if os.path.isfile(fpath):
        try:
            seting_f = open(fpath, "r")
            is_start = False
            nfield = 0
            line = "start"
            while line != "":
                line = seting_f.readline().strip()
                if is_start and line != "":
                    linearr = line.split()
                    if len(linearr) == nfield:
                        myuser = piuser(linearr[1], linearr[2], linearr[3], linearr[4])
                        user_list.append(myuser)
                        counter = counter + 1

                if line.find("[username]") != -1:
                    nfieldline = seting_f.readline().strip()  # IDNUM USERNAME CHATID TYPE TIME
                    nfield = len(nfieldline.split())
                    is_start = True
            seting_f.close()
        except IOError:
            print("Could not open file!")

    return counter


def checkSyntax(mystr):
    flag = True
    while True:
        if re.search("[+\-*/=!#$%&^~|()<>?\s]", mystr):
            flag = False
            break
        else:
            break
    return flag

def checkUserValid(chatid):
    for myuser in user_list:
        if str(chatid) == str(myuser.id):
            return True

    return False


def checkUserType(chatid):
    for myuser in user_list:
        if str(chatid) == str(myuser.id):
            return myuser.type
    return ""


def sendTextToAll(mode, msg):
    if msg == "":
        return False

    if mode == 1: #only for admin
        for user in user_list:
            if user.type == "admin":
                bot.sendMessage(int(user.id), msg)
    else: #send to all
        for user in user_list:
            bot.sendMessage(int(user.id), msg)


def docommand(chatid, cmd):
    global precmd
    global cmdstage
    global help_msg

    ret = help_msg
    cmd = cmd.lower()

    # pivpn command
    if cmd == '/listclient':
        ret = pivpnListClient(chatid)
    elif cmd == '/listconnection':
        ret = pivpnListConnection()
    elif cmd == '/listclientall':
        ret = pivpnListClientAll(chatid)
    elif cmd == '/addclient':
        ret = "Please input client name (no space) you want to create: "
    elif cmd == '/delclient':
        ret = "Please input client name (no space) you want to delete:"
    elif cmd == '/getovpn':
        ret = "Please input client name (no space) you want to get ovpn profile:"
    elif cmd == '/getinfo':
        ret = getInfo(chatid)

    # Admin management command
    elif cmd == '/adduser':
        ret = "Please input user in you want to add with syntax below: \n \
               <yourname> <chatid> <usertype> \n \
                yourname, chatid, usertype(admin/normal) without space \n \
                Ex: mariao 123456789 admin \n \
              "
    elif cmd == '/deluser':
        ret = "Please input username (no space) you want to add: "
    elif cmd == '/listuser':
        ret = listUser(chatid)
    elif cmd == '/logcmd':
        ret = "1: get log file, 2: clear log"

    elif cmd == '/setdns':
        ret = "Input dns address: "
    elif cmd == '/reboot':
        ret = "Are you sure reboot ? (yes/no): "
    elif cmd == '/restartnetwork':
        ret = restartNetwork(chatid)

    # HELP
    elif cmd == '/help':
        ret = getHelp(chatid)

    # Command with input para
    elif precmd == '/addclient':
        ret = pivpnAddClient(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/delclient':
        ret = pivpnDelClient(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/getovpn':
        ret = getOvpn(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/adduser':
        cmdarr_ = cmd.split()
        if len(cmdarr_) == 3:
            ret = addUser(chatid, cmdarr_[0], cmdarr_[1], cmdarr_[2])
        else:
            ret = "input parameter syntax error !!!"
        precmd = ""
        return ret
    elif precmd == '/deluser':
        ret = delUser(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/setdns':
        ret = setDns(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/logcmd':
        ret = logCmd(chatid, cmd)
        precmd = ""
        return ret
    elif precmd == '/reboot':
        if cmd == "yes" or cmd == "y":
            ret = reboot(chatid)
        else:
            ret = "Canceled !!!"
        precmd = ""
        return ret
    else:
        ret = help_msg

    precmd = cmd
    return ret


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['chat']['first_name']

    ts = time.gmtime()
    logmsg = time.strftime("%Y-%m-%d %H:%M:%S", ts) + " : sender: " + sender + ", chatid: " + str(chat_id) + ", command: " + command

    print(logmsg)

    logpath = WORKING_FOLDER + "log.txt"

    if not checkUserValid(chat_id):
        os.system("echo " + logmsg + " Invalid user >> " + logpath)
        bot.sendMessage(chat_id, "Permission denied, You can not user this bot !!!")
    else:
        os.system("echo " + logmsg + " >> " + logpath)
        bot.sendMessage(chat_id, docommand(chat_id, command))


# ------START TELEBOT-------
WORKING_FOLDER = "/home/pi/ovpns/"
help_msg = "/help for more information ! > ! <"
precmd = "None"
cmdstage = 0
user_list = []
TELEBOT_TOKEN = ""
if not getTelebotToken():
    print("can not get telebot token !!!")
    exit(1)

getUserlistInit()
bot = telepot.Bot(TELEBOT_TOKEN)
bot.message_loop(handle)
#sendTextToAll(1, "Hi, I am back ...")
while 1:
    time.sleep(1000)


