import tkinter as tk
from tkinter import filedialog
from upload_script import *
import subprocess

def open_file():
   file = filedialog.askopenfilename()
   if file:
      filename.insert(0,file)

def upload_file():
   base_url = "http://{}:{}/api/v1".format(ip.get(), port.get())
   token = get_token(base_url)
   status = get_status(base_url, token)
   while status.status_code == 204:
      status = get_status(base_url, token)
   post_file(base_url, token, filename.get())

window = tk.Tk()

label_a = tk.Label(text="Select file to be transfered")
label_a.grid(row=0,column=0,columnspan=2)

ip_label = tk.Label(text="Snapmaker IP")
ip_label.grid(row=1,column=0)
port_label = tk.Label(text="Port")
port_label.grid(row=2,column=0)
file_button = tk.Button(text="File",command=open_file)
file_button.grid(row=3,column=0)

ip = tk.Entry()
ip.grid(row=1,column=1)
ip.insert(0,"192.168.50.20")
port = tk.Entry()
port.grid(row=2,column=1)
port.insert(0,8080)
filename = tk.Entry()
filename.grid(row=3,column=1)

upload_button = tk.Button(text="Upload",command=upload_file)
upload_button.grid(row=4,column=1, columnspan=2,sticky="w")

window.mainloop()