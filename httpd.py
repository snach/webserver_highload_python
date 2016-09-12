import asyncore
import sys, getopt
import os
import socket
from utils import *

DOCUMENT_ROOT = 'static'
CPU_QTY = 1
SEND_BUFFER_SIZE = 8192

class Handler(asyncore.dispatcher):
    def __init__(self, client, path):
        self.path = path
        asyncore.dispatcher.__init__(self, client)
        self.data_to_write = []

    def handle_read(self):
        readed_data = self.recv(SEND_BUFFER_SIZE)

        if readed_data == '':
            self.send(make_response(405))
            self.close()
            return

        frst_str_data = readed_data.split('\n')[0]
        index_begin_HTTP = frst_str_data.rfind('HTTP')
        method = frst_str_data.split()[0]
        http_ver = frst_str_data[index_begin_HTTP + 5 : len(frst_str_data)]
        path = frst_str_data[len(method) + 1 : index_begin_HTTP - 1]


        '''print('method:' + method)
        print('path:' + path)
        print('http:' + http_ver)'''



        self.send('<html><head><title>200</title></head><body><h1>200 Hello Snach!</h1></body></html>')
        self.close()

    '''def writable(self):
        if self.data_to_write is not None:
            return True
        else:
            return False

    def handle_write(self):
        data = self.data_to_write.pop()

        sent_data = self.send(data[:SEND_BUFFER_SIZE])
        if sent_data < len(data):
            remaining = data[sent_data:]
            self.data_to_write.append(remaining)

        if not self.writable():
            self.handle_close()'''

class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(500)
        print('Start server: ' + host + ':' + str(port) )

    def handle_accept(self):

        client,addr = self.accept()
        print('Incoming connection from %s' % repr(addr))
        Handler(client, addr)




if __name__ == '__main__':
    try:
        myopts, args = getopt.getopt(sys.argv[1:], "r:c:")
        for o, a in myopts:
            if o == '-r':
                DOCUMENT_ROOT = a
            elif o == '-c':
                CPU_QTY = int(a)

        server = Server('localhost', 80)
        for i in range(1, CPU_QTY):
            os.fork()
        asyncore.loop(timeout=0.1)

    except KeyboardInterrupt:
        print('\nBye')
        sys.exit(0)