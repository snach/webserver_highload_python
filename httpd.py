import asyncore
import sys, getopt
import os
import socket
import mimetypes
import urllib
from utils import *

SERVER = 'localhost'
PORT = 80
DOCUMENT_ROOT = 'static'
CPU_QTY = 1
SEND_BUFFER_SIZE = 4096


class Handler(asyncore.dispatcher):
    def __init__(self, client, path):
        self.path = path
        asyncore.dispatcher.__init__(self, client)
        self.data_to_write = []

    def handle_read(self):
        readed_data = self.recv(SEND_BUFFER_SIZE)
        readed_data = urllib.unquote(readed_data)
        print('READED_DATA!!!!\n' + readed_data)

        if readed_data == '':
            self.send(make_response(405))
            self.close()
            return

        frst_str_data = readed_data.split('\n')[0]
        index_begin_HTTP = frst_str_data.rfind('HTTP')
        method = frst_str_data.split()[0]
#        http_ver = frst_str_data[index_begin_HTTP + 5 : len(frst_str_data)]
        path = frst_str_data[len(method) + 1 : index_begin_HTTP - 1]

        print(method)


        if 'get' in method.lower() or 'head' in method.lower():

            if '?' in path:
                path = path.split('?')[0]
            path_to_local_data = DOCUMENT_ROOT + '/' + path
            print(path_to_local_data)
        else:

            self.send(make_response(405))
            self.close()
            return

        if '../' in path_to_local_data:
                self.send(make_response(403))
                self.close()
                return

        if not os.path.exists(path_to_local_data):
            print(make_response(404))
            self.send(make_response(404))
            self.close()
            return
        else:



            if os.path.isdir(path_to_local_data):
                path_to_local_data += 'index.html'


            print(path_to_local_data)


            try:
                #print('i\'m here')
                file = open(path_to_local_data, 'r').read()
            except IOError:
                print(make_response(403))
                self.send(make_response(403))
                self.close()



            size_of_file = os.path.getsize(path_to_local_data)
            type_of_file = mimetypes.guess_type(path_to_local_data, strict=True)[0]

            response = make_response(200, str(type_of_file), str(size_of_file))
            #print(response)
            print('RESPONSE!!!!!!!!!!!!\n' + response)


            if 'head' in method.lower():
                print('im in need if, my method:'+ method + '!!!!!!!!!!' )
                self.send(response)
                self.close()
            else:
                response += file

            self.data_to_write.append(response)

    def writable(self):
        return bool(self.data_to_write)


    def handle_write(self):
        data = self.data_to_write.pop()

        sent = self.send(data[:SEND_BUFFER_SIZE])
        if sent < len(data):
            remaining = data[sent:]
            self.data_to_write.append(remaining)

        if not self.writable():
            self.handle_close()

class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(500)
        print('Start server: ' + host + ':' + str(port) )

    def handle_accept(self):

        try:
            client, addr = self.accept()
            print('Incoming connection from %s' % repr(addr))
            Handler(client, addr)
        except:
            return




if __name__ == '__main__':
    try:
        args_com_line, args = getopt.getopt(sys.argv[1:], "r:c:")
        for option, arg in args_com_line:
            if option == '-r':
                DOCUMENT_ROOT = arg
            elif option == '-c':
                CPU_QTY = int(arg)

        server = Server(SERVER, PORT)
        for i in range(1, CPU_QTY):
            os.fork()
        asyncore.loop(timeout=0.1)

    except KeyboardInterrupt:
        print('\nBye')
        sys.exit(0)