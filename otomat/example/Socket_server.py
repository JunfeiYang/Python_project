
import SocketServer
import  commands
import  time

class Myhander(SocketServer.BaseRequestHandler)
    def handle(self):
        while 1:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                print "Client %s is dead" % (self.client_address[0])
                break
            user_input = self.data.split()
            if user_input[0] == 'get':
                print "Startig to transfer files"
                with open(user_input[1],'rb') as f:

                    self.request.sendall(f.read())
                time.sleep(0.5)
                self.request.send('otomat')
                continue
            cmd_status,result = commands.getstatusoutput(self.data)
            if len(result.strip()) != 0:
                self.request.sendall('Done')

if __name__=="__main__":
    HOST,PORT = "localhost",8000
    server = SocketServer.ThreadingTCPServer((HOST,PORT),Myhander)
    server.serve_forever()

