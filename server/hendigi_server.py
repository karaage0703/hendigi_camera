# -*- coding:utf-8 -*-
import socket
import subprocess
import time

host = "karaage.local" #お使いのサーバーのホスト名を入れます
port = 8888 #クライアントと同じPORTをしてあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

print 'Waiting for connections...'
clientsock, client_address = serversock.accept() #接続されればデータを格納

while True:
    rcvmsg = clientsock.recv(1024)
    print 'Received -> %s' % (rcvmsg)
    if rcvmsg == '.':
        break
    if rcvmsg == 'go':
        clientsock.send("ok")
        photo_numb = clientsock.recv(1024)
        print ("photo_numb=" + photo_numb)
        print ("uploading...")
        cmd = "./download.sh " + photo_numb
        subprocess.call(cmd, shell=True)
        clientsock.sendall("downloaded")
        time.sleep(1.0)

        print ("processing...")
        cmd = "./deeplearning.sh " + photo_numb
        subprocess.call(cmd, shell=True)

        rcvmsg = clientsock.recv(1024)
        print 'Received -> %s' % (rcvmsg)

        clientsock.sendall("processed")
        time.sleep(1.0)

        print ("downloading...")
        cmd = "./upload.sh " + photo_numb
        subprocess.call(cmd, shell=True)
        clientsock.sendall("uploaded")

clientsock.close()
