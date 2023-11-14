import socket, json, random, datetime, hashlib, sys

def handle_get():
    return "in get"

def isValid(username, password):
    file = open("passwords.json")
    data = json.load(file)

    for user in data:
        pw = data[user]
        if (username == user) and (password == pw):
            return True
        
    return False

def logMessage():
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    second = time.second

    return f"SERVER LOG: {year}-{month}-{day}-{hour}-{minute}-{second}"

def getRandom():
    num = random.getrandbits(64)
    hex_num = format(num, '016x')
    return hex_num

def handle_post(HTTPRequest, conn):
    lines = HTTPRequest.split("\r\n")
    
    username = lines[4].replace("username: ", "")
    password = lines[5].replace("password: ", "")

    if username == "" or password == "":
        conn.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
        print(logMessage() + " LOGIN FAILED")

    if(isValid(username, password)):
        sessionID = "sessionID=0x" + getRandom()
        message = f"HTTP/1.0 200 OK\r\nSet-Cookie: {sessionID}\r\n\r\nLogged in!"
        conn.send(message.encode())
        print(logMessage() + f" LOGIN SUCCESSFUL: {username} : {password}")

    return

def start_server(IP, PORT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            HTTPRequest = conn.recv(1024).decode("ascii")

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
                s.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())

            conn.close()
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