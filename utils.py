import datetime

HTTP_VER = '1.1'
SERVER = 'snacheva_localhost'


def make_response(status_code,
                  content_type='text/html; charset=UTF-8', content_length=''):
    response = 'HTTP/' + HTTP_VER

    if status_code == 400:
        response += ' 400 Bad Request'
    elif status_code == 403:
        response += ' 403 Forbidden'
    elif status_code == 404:
        response += ' 404 Not Found'
    elif status_code == 405:
        response += ' 405 Method Not Allowed'
    elif status_code == 200:
        response += ' 200 OK'

    response += '\r\nServer: ' + SERVER + '\r\n'
    response += 'Date: ' + str(datetime.datetime.now()) + '\r\n'
    response += 'Content-Type: ' + content_type + '\r\n'
    response += "Connection: close\r\n"

    if status_code == 200:
        response += "Content-Length: " + content_length + "\r\n"

    response += "\r\n"

    if status_code == 400:
        response += "<html><head><title>400</title></head><body><h2>Bad Request</h2></body></html>"
    elif status_code == 403:
        response += "<html><head><title>403 Forbidden</title></head><body><h1>403 Forbidden</h1></body></html>"
    elif status_code == 404:
        response += "<html><head><title>404 Not found</title></head><body><h2>404 Not found</h2></body></html>"
    elif status_code == 405:
        response += "<html><head><title>405</title></head><body><h2>405 Method Not Allowed</h2></body></html>"

    return response
