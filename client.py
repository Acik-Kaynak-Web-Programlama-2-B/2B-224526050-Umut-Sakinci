from socket import * 
from threading import *
from tkinter import *
from datetime import datetime  
from tkinter import filedialog

client = socket(AF_INET, SOCK_STREAM)

ip = "10.100.5.151"
port = 3333

client.connect((ip, port))

window = Tk()
window.configure(bg='blue')

window.title("Bağlandı: "+ ip)

message = Text(window, width=50, background='lightblue')
message.grid(row =0, column=0, padx=10, pady=10,)

message_entry = Entry(window, width=50)
message_entry.insert(0, "Adınız *")

message_entry.grid(row=1,column=0,padx=10,pady=10)

message_entry.focus()
message_entry.selection_range(0, END)

def mesaj_gonder():
    client_message = message_entry.get()
    message.insert(END, '\n' + 'Sen :'+ client_message)
    client.send(client_message.encode('utf8'))
    message_entry.delete(0, END)
    
def dosya_gonder():
    file_name = filedialog.askopenfilename()
    client.send(file_name.encode('utf8'))

    with open(file_name, 'rb') as file:
        for data in file:
            client.send(data)
    print(f"{file_name} dosyası gönderildi.")
    
btn_msj_gonder = Button(window, text="Gönder", width=30, command=mesaj_gonder)
btn_msj_gonder.grid(row=2, column=0, pady=10,padx=10)

btn_dosya_gonder = Button(window, text="Dosya Gönder", width=30, command=dosya_gonder)
btn_dosya_gonder.grid(row=3, column=0, pady=10, padx=10)
    
def gelen_msaj_kontrol():
    while True:
        server_msg = client.recv(1024).decode('utf8')
        message.insert(END, '\n'+ server_msg)
        
        
window.bind('<Return>', lambda event=None: btn_msj_gonder.invoke())
        
recv_kontrol = Thread(target=gelen_msaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()

window.mainloop()
        