from socket import *
import sys
import time

class Log:
    
    def push(self, t, msg):
        if t == 'WARNING':
            print '[!] %s' %(msg)
        elif t == 'REQUEST':
            print '[<] %s' %(msg)
        elif t == 'RESPONSE':
            print '[>] %s' %(msg)
        else:
            print '[i] %s' %(msg)

class Server:
    
    HOST = None
    PORT = None
    SERVER = None
    LOG = None
    CLIENT = None

    def __init__(self):
        
        # Ubersimple parametercheck, no validation
        if len(sys.argv) < 3:
            sys.exit('[X] Insufficient arguments. (webserver2.py <host> <port>)')
        else:
            self.HOST = sys.argv[1]
            self.PORT = int(sys.argv[2])
            self.SERVER = socket(AF_INET, SOCK_STREAM)
            self.LOG = Log()

    def bind(self):
        
        # Bind the a socket to the server on host system and listen with 1 queue spot

        try:
            self.SERVER.bind((self.HOST, self.PORT))
        except error, msg:
            sys.exit('[X] Bind failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])

        self.SERVER.listen(1)

        self.LOG.push('INFO', 'Webserver initialized. (%s:%d)' %(self.HOST, self.PORT))

    def write(self, status, msg, data):
        
        # Generate a HTTP Response and push to conn

        data_concat = '\n'.join(data)

        self.CLIENT.send('HTTP/1.1 ' + status + ' ' + msg + '\n')
        self.CLIENT.send('Connection: close\n')
        self.CLIENT.send('Content-Type: text/html; charset=utf8\n')
        self.CLIENT.send('Content-Length: ' + str(len(data_concat)) + '\n\n')

        self.LOG.push('RESPONSE', 'Sending response bytes %d' %(len(data_concat)))

        self.CLIENT.send(data_concat)

    def read_file(self, filename):

        # Read the file requested by connection

        try:
            f = open(filename, 'r')
            self.write('200', 'OK', f.readlines())
        except IOError:
            self.LOG.push('WARNING', 'Requested file: %s not found.' %(filename))
            self.write('404', 'Not found', [])

    def parse_req(self, req):

        # Extract the requested file

        req = req.split()
        filename = req[1][1:]

        self.read_file(filename)

    def run(self):

        # Main run loop

        try:
            while True:
                self.LOG.push('INFO', 'Awaiting connections...')

                connection, addr = self.SERVER.accept()

                self.CLIENT = connection

                self.LOG.push('INFO', 'Connected to %s (%s)' %(addr[0], str(addr[1])))

                
                request = connection.recv(4096)
                self.LOG.push('REQUEST', 'Request:')
                    
                lines = request.split('\n')

                for line in lines:
                    print '\t' + line

                self.parse_req(lines[0])

                connection.close()

        except KeyboardInterrupt:
            print '\n[X] Detected interrupt, shutting down'

            self.LOG.push('WARNING', 'Destroying serversocket...')
            self.SERVER.close()
            server.LOG.push('INFO', 'Done, exiting...')

            sys.exit(0)

# Create server object, bind and run

try:
    server = Server()
    server.bind()
    server.run()

except KeyboardInterrupt:
    print '\n[X] Detected interrupt, shutting down...'
    
    server.LOG.push('WARNING', 'Destroying serversocket...')
    server.SERVER.close()

    server.LOG.push('INFO', 'Done, exiting.')

    sys.exit(0)
