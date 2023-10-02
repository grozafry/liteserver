# Uncomment this to pass the first stage
import socket


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
    conn, addr = server_socket.accept()

    print(f"After accepting connection")
    print(f"Client Socket object is {conn}.")
    print(f"Connection has been received from IP - {addr[0]}, PORT - {addr[1]}")
    print(f"IP is my IP as visible to the server system. Same with PORT.")
    print(f"If you access from browser, OS/Chrome will assign a random port number for creating an outgoing connection.")


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
    if path == '/':
        conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    else:
        conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')


if __name__ == "__main__":
    main()
