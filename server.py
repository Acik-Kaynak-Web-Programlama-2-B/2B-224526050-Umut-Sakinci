from socket import *
from threading import *

clients = []
names = []

def clientThread(client):
    bayrak = True
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            if bayrak:
                names.append(message)
                print(message, 'bağlandı')
                bayrak = False
            for c in clients:
                if c != client:
                    index = clients.index(client)
                    name = names[index]
                    c.send((name + ':' + message).encode('utf8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            name=names[index]
            names.remove(name)
            print(name + ' çıktı')
            break
        

def file_transfer_thread(client):
    try:
        filename = client.recv(1024).decode('utf8')
        print(f"Alınan dosya adı: {filename}")
        with open(filename, 'wb') as file:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"{filename} dosyası başarıyla alındı.")
    except:
        print("Dosya transferi sırasında bir hata oluştu.")
        
        
        
server = socket(AF_INET, SOCK_STREAM)

ip = "10.100.5.151"
port = 3333
server.bind((ip, port))
server.listen()
print('Server Dinlemede')



while True:
    client, adress = server.accept()
    clients.append(client)
    print('Bağlantı Yapıldı', adress[0] + ':' + str(adress[1]))
    thread = Thread(target = clientThread, args=(client,))
    thread.start()         
    file_transfer_thread = Thread(target=file_transfer_thread, args=(client,))
    file_transfer_thread.start()
       