from socket import *
import time
from sys import stdout, stdin, exit, exc_info
import ssl
import base64
import getpass

# Change this to whatever you want to display in the From: header
REALNAME = 'Aleksander'

# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

class MailClient:
 
    """ The MailClient class initiates and connects to gmail via SMTPS (SSL) and lets the user send one mail per run """

    host = (None, None)
    socket = None
    logtype = {u'info': C + '[' + W + 'i' + C + '] (' + W + '%s' + C + ') %s\r\n' + W,
               u'error': R + '[' + W + 'X' + R + '] (' + W + '%s' + R + ') %s\r\n' + W,
               u'warning': O + '[' + W + '!' + O + '] (' + W + '%s' + O + ') %s\r\n' + W,
               u'input': B + '[' + W + '?' + B + '] (' + W + '%s' + B + ') %s' + W,
               u'success': G + '[' + W + '>' + G + '] (' + W + '%s' + G + ') %s\r\n' + W}

    # Wrap a socket in SSL, set host tuple and draw intro
    def __init__(self):
        self.socket = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
        self.host = ('smtp.gmail.com', 465)
        self.intro()

    # Push some text to stdout
    def log(self, lt, msg):
        stdout.write(self.logtype[lt] %(time.strftime('%H:%M:%S'), msg))
        stdout.flush()

    # ooOOooOoooOOoooOo fancy...
    def intro(self):
        print ''
        print B + '-------- ' + W + 'UberMail v1.0' + B + ' ---------------------------------------------------'
        print ''
        self.log('info', 'Mail client initialized, connecting to ' + W + '%s:%d' %(self.host[0], self.host[1]) + C + '...')
        print ''

    # Connect to host or die
    def connect(self):
        try:
            self.socket.connect(self.host)
            self.log('success', 'Connected to ' + W + '%s:%d' %(self.host[0], self.host[1]) + W)
        except error, msg:
            self.log('error', '[' + str(msg[0]) + '] ' + msg[1])
            exit()


    # Check for closed socket, error statuses, and return newline-stripped string
    def check(self, data):
        if not data:
            self.disconnect('Connection closed by server, shutting down...')
        elif int(data[:3]) >= 500:
            self.disconnect(data)
        return data.strip()

    # Send a server command, parse / check the result and spit it back
    def send_and_parse(self, msg):
        self.socket.send(msg + '\r\n')
        return self.check(self.socket.recv(2048))

    # Main run method
    def run(self):
        
        # Grab some initial bytes...
        data = self.socket.recv(2048)
        self.check(data)
        
        # Show a warning if the server fails to grant the 220 Connection reply
        if data[:3] != '220':
            self.log('warning', '220 Reply NOT recieved from server.')
        
        # Fire away the modified HELO command that exposes available server features
        self.log('info', data)
        data = self.send_and_parse('EHLO localhost').split('\n')

        # Show a warning if line does not contain a 250 OK message
        for line in data:
            if '250' not in line:
                self.log('warning', '250 Reply NOT recieved on ' + line)
            else:
                self.log('info', line)


        # Fetch user credentials from stdin
        self.log('input', 'Enter your email adress: ')
        mail = raw_input()
        mail = mail.strip()
        self.log('input', 'Enter your ')
        pasw = getpass.getpass()
        pasw = pasw.strip()

        self.log('info', 'Attempting to login with: ' + W + mail + C + ' and ' + W + ''.join(['*' for x in range(len(pasw))]))

        # Perform the login
        self.log('info', self.send_and_parse('AUTH LOGIN'))
        self.log('info', self.send_and_parse(base64.b64encode(mail)))
        data = self.send_and_parse(base64.b64encode(pasw))

        # Authenticate or die
        if '235' not in data:
            self.disconnect(data)
        else:
            self.log('success', 'Successfully logged in. ' + data)
        
        # Write some initial mail commands and set up for the DATA part...
        self.log('success', self.send_and_parse('MAIL FROM: <' + mail + '>'))
        self.log('input', 'Enter the recipient(s) email adress: ')
        rcpt = raw_input()
        self.log('success', self.send_and_parse('RCPT TO: <' + rcpt + '>'))
        data = self.send_and_parse('DATA')
        
        # Display the 354 Go Ahead response
        self.log('info', data)

        # Write the headers
        self.socket.send('To: ' + rcpt + '\r\n')
        self.socket.send('From: ' + REALNAME + ' <' + mail + '>\r\n')
        self.log('input', 'Enter subject: ')
        subj = raw_input()
        self.log('input', 'Enter your message:\n')
        mesg = raw_input()
        self.socket.send('Content-Type: text/plain\r\n')
        self.socket.send('Subject: ' + subj.strip() + '\r\n')
        self.socket.send('\r\n')
        self.socket.send(mesg.strip() + '\r\n')
        data = self.send_and_parse('\r\n.')
        
        # Succeed or die, dump message to stdout
        if '250' not in data:
            self.disconnect(data)
        else:
            self.log('success', data)
            self.log('success', 'Your mail was successfully sent to ' + W + rcpt)

        
        # Send the quit message and let the recv method do its trick to trigger the "if not data" check
        data = self.send_and_parse('QUIT')
        self.log('info', data)
        data = self.socket.recv(2048)
        data = self.check(data)

    # Destroys the client socket and shuts down
    def disconnect(self, reason):
        self.log('warning', reason)
        self.socket.close()
        self.log('info', 'Shutdown complete!')
        exit()

# Start and run the client
mc = MailClient()
try:
    mc.connect()
    mc.run()
except KeyboardInterrupt:
    mc.disconnect('Detected interrupt, shutting down...')
