import socket, json, random, datetime, hashlib, sys

def start_server(IP, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            HTTPRequest = conn.recv(1024).decode("ascii")
            print(HTTPRequest)

def main():
    IP = sys.argv[1]
    PORT = int(sys.argv[2].strip(""))
    ACCOUNTS_FILE = sys.argv[3]
    SESSION_TIMEOUT = sys.argv[4]
    ROOT_DIRECTORY = sys.argv[5]

    start_server(IP, PORT)

if __name__ == '__main__':
    main()