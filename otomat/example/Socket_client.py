
import socket,time

HOST = '172.16.209.111'
PORT = 8000

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

while 1:
    cmd = raw_input("Your command:").strip()
    if len(cmd) == 0:
        break
    s.sendall(cmd)
    if cmd.split()[0] == 'get':
        print   "Start downloading file......"
        with open(cmd.split()[1],'wb') as f:
            while 1:
                data = s.recv(1024)
                if data == "otomat":break
                f.write(data)
        continue
    else:
        print s.recv(1024)
s.close()