import socket
import threading
import time
from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import pickle
import rsa
import binascii


def set_ip():
    global name
    name = name_text.get()
    ip = edit_text_ip.get()
    port = edit_text_port.get()
    print(ip,port)
    
    # Define Server:
    server = socket.socket()
    server.bind((ip, int(port)))
    server.listen()

    global conn
    conn, addr = server.accept()

    input_root.destroy()

    input_root.quit()

def send():
    if str(edit_text.get()).strip() != "":
        message = str.encode(edit_text.get())
        #converting it into number
        hex_data   = binascii.hexlify(message)
        plain_text = int(hex_data, 16)
        ctt=rsa.encrypt(plain_text,pkey)
        conn.send(str(ctt).encode())
        # message alignment
        listbox.insert(END,"{:>90}".format(message.decode("utf-8")))
        edit_text.delete(0, END)


        # after message is sent
        edit_text.delete(0, END)


def recv():
    while True:
        response_message =int(conn.recv(1024).decode())
        print(response_message)
        decrypted_msg = rsa.decrypt(response_message, private)
        # inserting message received from the sender:
        listbox.insert(END, name1 +" : "+ str(decrypted_msg))
        edit_text.delete(0, END)

# Server GUI:
public, private = rsa.generate_keypair(1024)
msg=pickle.dumps(public)

# 1: Input Root GUI
input_root = Tk()

bgimage = PhotoImage(file ="ab.png", height="500", width="400")
Label(input_root,image=bgimage).place(relwidth=1,relheight=1)

input_root.grid_columnconfigure((0,4), weight=1)
input_root.grid_rowconfigure((0,0), weight=1)
input_root.grid_rowconfigure((2,0), weight=1)
input_root.grid_rowconfigure((4,0), weight=1)
input_root.grid_rowconfigure((6,0), weight=1)

logo = Image.open("logo1.gif")
resized = logo.resize((100,100),Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
Label_logo= Label(input_root,image=image)
Label_logo.grid(row=0, column=1, columnspan=3)

name_text = tk.Entry(input_root, bd=4, font=("Arial", 14), bg="misty rose")
edit_text_ip = tk.Entry(input_root, bd=4, font=("Arial", 14), bg="misty rose")
edit_text_port = tk.Entry(input_root, bd=4, font=("Arial", 14), bg="misty rose")

name_label =  tk.Label(input_root, text="Enter Name:", font=("Arial", 14))
ip_label = tk.Label(input_root, text="Enter IP:", font=("Arial", 14))
port_label = tk.Label(input_root, text="Enter Port:", font=("Arial", 14))

connect_btn = tk.Button(input_root,
                        text="Connect",
                        command=set_ip,
                        activebackground="plum1",	
                        activeforeground="purple",
                        bg="plum1",
                        bd="3",
                        relief="raised",
                        fg="DeepPink4",
                        font=("Arial", 14, "bold"),
                        height=1,
                        width=28,
                        pady=2)


# show elements
name_label.grid(row=1,column=1)
name_text.grid(row=1,column=3)

ip_label.grid(row=3,column=1)
edit_text_ip.grid(row=3,column=3)

port_label.grid(row=5,column=1)
edit_text_port.grid(row=5,column=3)

connect_btn.grid(row=7,column=1, columnspan=3)

input_root.title("Chat App")
input_root.geometry("400x500")
input_root.resizable(width=False, height=False)

input_root.mainloop()


#sending details
conn.send(str.encode(name))
name1=conn.recv(1024).decode()
conn.send(msg)#sending public key
rmsg=conn.recv(1024)#receiving public key
pkey=pickle.loads(rmsg)
#print("public key of other is :",pkey[0])


# 2: Main Root GUI
root = Tk()

# Scrollbar implementation
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=BOTH)
scrollbar1 = Scrollbar(root,orient = tk.HORIZONTAL)
scrollbar1.pack(side=BOTTOM, fill=BOTH)
listbox = Listbox(root, bg="lavender blush",
                  selectbackground="HotPink4",
                  fg="dark slate gray",
                  highlightbackground="pink",
                  highlightcolor="MediumOrchid1",
                  highlightthickness="2",
                  font=('Bookman Old Style',14,'italic'),
                  height=20,
                  yscrollcommand=scrollbar.set,
                  xscrollcommand=scrollbar1.set)
listbox.pack(fill=BOTH, side=TOP)
scrollbar.config(command=listbox.yview)
scrollbar1.config(command=listbox.xview)

button = Button(root, text="Send Message",
                command=send,
                activebackground="PaleVioletRed3",	
                activeforeground="PaleVioletRed1",
                bg="MediumPurple4",
                bd="3",
                relief="raised",
                fg="white",
                font=("Arial", 14, "bold"),
                height=1,
                width=35,
                pady=2)
button.pack(fill=X, side=BOTTOM)

edit_text = Entry(root,
                  bd=4,
                  font=("Arial", 16),
                  bg="misty rose")
edit_text.pack(fill=X, side=BOTTOM)


root.title(name)
root.geometry("500x600")
root.resizable(width=True, height=True)

threading.Thread(target=recv).start()

root.mainloop()
