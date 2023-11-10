import socket, json, random, datetime, hashlib, sys

def handle_get():
    return "in get"

def handle_post(HTTPRequest, conn):
    lines = HTTPRequest.split("\r\n")
    username = lines[4]
    password = lines[5]

    if username == "" or password == "":
        conn.send("HTTP/1.0 501 Not Implemented\r\n".encode())
        print("LOGIN FAILED")

    return

def start_server(IP, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            HTTPRequest = conn.recv(1024).decode("ascii")
            #print(HTTPRequest)

            lineOne = HTTPRequest.split("\r\n")[0]
            lineOne = lineOne.split(" ")
            HTTPCommand = lineOne[0]
            RequestTarget = lineOne[1]
            HTTPVersion = lineOne[2]

            if HTTPCommand == "POST" and RequestTarget == "/":
                handle_post(HTTPRequest, conn)
            elif HTTPCommand == "GET":
                print(handle_get())
            else:
                #send “501 Not Implemented”
                s.send("HTTP/1.0 501 Not Implemented\r\n".encode())

            s.close()
            exit()

def main():
    IP = sys.argv[1]
    PORT = int(sys.argv[2].strip(""))
    ACCOUNTS_FILE = sys.argv[3]
    SESSION_TIMEOUT = sys.argv[4]
    ROOT_DIRECTORY = sys.argv[5]

    start_server(IP, PORT)

if __name__ == '__main__':
    main()