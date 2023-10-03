# # Uncomment this to pass the first stage
# import socket
# import re


# def main():
#     # You can use print statements as follows for debugging, they'll be visible when running tests.
#     print("Logs from your program will appear here!")

#     # Uncomment this to pass the first stage
#     #
#     server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
#     print(f"Before accepting connection")
    
#     # server_socket.accept() 
#     #This is a blocking operation, kind-of-like time.sleep() 
#     #in the sense that it will block code exexcuti  on until a connection is accepted.
    
#     #On acceptance of a connection from the backlog queue ( server_socket.listen(5) where 5 is the backlog_queue_size )
#     #client_socket details are returned
#     conn, addr = server_socket.accept()

#     print(f"After accepting connection")
#     print(f"Client Socket object is {conn}.")
#     print(f"Connection has been received from IP - {addr[0]}, PORT - {addr[1]}")
#     print(f"IP is my IP as visible to the server system. Same with PORT.")
#     print(f"If you access from browser, OS/Chrome will assign a random port number for creating an outgoing connection.")


#     data = conn.recv(1024)
#     #This is again a blocking operation
#     #Wait until received max 1024 bytes of data from conn client_socket. 
#     #If more data is to be received, use this statements again.
#     #Note - This is connection data, not just request data

#     print(f"Connection data received from the client connection socket in first batch of  max 1024 bytes is {data}")

#     # conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
#     # sendall() is a method provided by socket objects in Python. 
#     # It is used to send data from the server to the connected client. 
#     # Unlike send(), which may not send all the data at once, sendall() 
#     # ensures that all the data is sent and retries if necessary until 
#     # all the data has been transmitted or an error occurs.

#     #Note - Here we are only sending 'HTTP Status Line' in our connection response. 
#     #We can also add a 'response body' like this - conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nThis is response body")
#     #\r\n\r\n is a separator between 'HTTP Status Line' and 'response body'


#     path = data.decode("utf-8").split('\r\n')[0].split(" ")[1]
#     # if path == '/':
#     #     conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
#     # else:
#     #     conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

#     # GET /echo/<a-random-string>

#     if path == '/':
#         conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
#     elif path == '/user-agent':
#         lines = data.decode("utf-8").split('\r\n')
#         user_agent = list(filter(lambda x: True if x.split(":")[0] == 'User-Agent' else False, lines))[0].split(":")[-1].strip()
#         print(f"User-Agent is {user_agent}")
#         response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {user_agent.__len__()}\r\n\r\n{user_agent}'.encode(encoding='utf-8')
#         conn.sendall(response)

#     elif re.match('/echo/*', path):
#         random_string = path.replace('/echo/','')
#         content_length = len(random_string)
#         response = bytes(f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{random_string}', encoding='UTF-8')
#         conn.sendall(response)
#     # else:
#     #     conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

    
#     # elif re.match('/echo/*', path):
#     #     random_string = path.replace('/echo/','')
#     #     content_length = len(random_string)
#     #     response = bytes(f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{random_string}', encoding='UTF-8')
#     #     conn.sendall(response)
#     else:
#         conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')


# if __name__ == "__main__":
#     main()


###############----------------HANDLING----CONCURRENT----CONNECTIONS-------------#################
# Uncomment this to pass the first stage
import socket
import re
import threading
import sys
import os

def conn_listener(conn, addr):
    print(f"conn_listener now active for client_socket on IP {addr[0]} and PORT {addr[1]}")
    data = conn.recv(1024)
    #This is again a blocking operation
    #Wait until received max 1024 bytes of data from conn client_socket. 
    #If more data is to be received, use this statements again.
    #Note - This is connection data, not just request data

    print(f"Connection data received from the client connection socket in first batch of  max 1024 bytes is {data}")

    # conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    # sendall() is a method provided by socket objects in Python. 
    # It is used to send data from the server to the connected client. 
    # Unlike send(), which may not send all the data at once, sendall() 
    # ensures that all the data is sent and retries if necessary until 
    # all the data has been transmitted or an error occurs.

    #Note - Here we are only sending 'HTTP Status Line' in our connection response. 
    #We can also add a 'response body' like this - conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nThis is response body")
    #\r\n\r\n is a separator between 'HTTP Status Line' and 'response body'


    path = data.decode("utf-8").split('\r\n')[0].split(" ")[1]
    # if path == '/':
    #     conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    # else:
    #     conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

    # GET /echo/<a-random-string>

    if path == '/':
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    elif path == '/user-agent':
        lines = data.decode("utf-8").split('\r\n')
        user_agent = list(filter(lambda x: True if x.split(":")[0] == 'User-Agent' else False, lines))[0].split(":")[-1].strip()
        print(f"User-Agent is {user_agent}")
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {user_agent.__len__()}\r\n\r\n{user_agent}'.encode(encoding='utf-8')
        conn.sendall(response)

    elif re.match('/echo/*', path):
        random_string = path.replace('/echo/','')
        content_length = len(random_string)
        response = bytes(f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{random_string}', encoding='UTF-8')
        conn.sendall(response)

    elif path.split("/")[1] == "files":
        fileName = path[6:]
        print("File Name = ", fileName)
        directory = sys.argv[-1]
        if os.path.exists(directory + fileName):
            file = open(directory + fileName, "rb")
            body = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {os.path.getsize(directory + fileName)}\r\n\r\n"
            conn.send(body.encode())
            conn.send(file.read())
            file.close()
        else:
             conn.send(b"HTTP/1.1 404 Not Found \r\n\r\n")
    # else:
    #     conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

    
    # elif re.match('/echo/*', path):
    #     random_string = path.replace('/echo/','')
    #     content_length = len(random_string)
    #     response = bytes(f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{random_string}', encoding='UTF-8')
    #     conn.sendall(response)
    else:
        conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')
    print(f"Closing connection for client_socket {conn} from PORT {addr[1]}")
    conn.close()  #This is impportant. Close connections once data has been received. So we can make more connections.

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    print(f"Before accepting connection")
    
    # server_socket.accept() 
    #This is a blocking operation, kind-of-like time.sleep() 
    #in the sense that it will block code exexcuti  on until a connection is accepted.
    
    #On acceptance of a connection from the backlog queue ( server_socket.listen(5) where 5 is the backlog_queue_size )
    #client_socket details are returned
    while True:
        conn, addr = server_socket.accept()
        # print(f"After accepting connection")
        # print(f"Client Socket object is {conn}.")
        # print(f"Connection has been received from IP - {addr[0]}, PORT - {addr[1]}")
        # print(f"IP is my IP as visible to the server system. Same with PORT.")
        # print(f"If you access from browser, OS/Chrome will assign a random port number for creating an outgoing connection.")
    
        thread = threading.Thread(target = conn_listener, args = (conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
