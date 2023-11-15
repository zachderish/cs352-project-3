import socket, json, random, datetime, hashlib, sys

sessions = {}

def handle_post(headers, conn):

    if (not "username" in headers.keys()) or (not "password" in headers.keys()):
        conn.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
        print(logMessage() + " LOGIN FAILED")

    username = headers["username"]
    password = headers["password"]
    if(isValid(username, password)):
        sessionID = "sessionID=0x" + getRandom()
        sessions[sessionID] = [getTime(), username]
        message = f"HTTP/1.0 200 OK\r\nSet-Cookie: {sessionID}\r\n\r\nLogged in!"
        conn.send(message.encode())
        print(logMessage() + f" LOGIN SUCCESSFUL: {username} : {password}")

    else:
        print(logMessage() + f" LOGIN FAILED: {username} : {password}")
        message = f"HTTP/1.0 200 OK\r\n\r\nLogin failed!"

def handle_get(headers, conn, SESSION_TIMEOUT):
    if not "Cookie" in headers.keys():
        message = "HTTP/1.0 401 Unauthorized\r\n\r\n"
        conn.send(message.encode())
    
    sessionID = headers["Cookie"].strip()
    if sessionID in sessions.keys():
        timestamp = sessions[sessionID][0]
        username = sessions[sessionID][1]
        currentTime = getTime()
        if(validTime(timestamp, currentTime, SESSION_TIMEOUT)):
            print("valid time")

        timeLength = len(currentTime)
        print("valid sessionID")

# will correct this
def validTime(timestamp, currentTime, SESSION_TIMEOUT):
    timestamp = timestamp.split("-")
    time1 = datetime.datetime(int(timestamp[0]), int(timestamp[1]), int(timestamp[2]), int(timestamp[3]), int(timestamp[4]), int(timestamp[5]))
    currentTime = currentTime.split("-")
    time2 = datetime.datetime(int(currentTime[0]), int(currentTime[1]), int(currentTime[2]), int(currentTime[3]), int(currentTime[4]), int(currentTime[5]))
    diff = time2 - time1
    if (int(diff.split(":")[2]) <= SESSION_TIMEOUT and diff.split(":")[0] == "0" and diff.split(":")[1] == "00"):
        return True
    else:
        return False

# check if username and password are valid
def isValid(username, password):
    file = open("passwords.json")
    data = json.load(file)

    for user in data:
        pw = data[user]
        if (username == user) and (password == pw):
            return True
        
    return False

# get current time 
def getTime():
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    second = time.second
    return f"{year}-{month}-{day}-{hour}-{minute}-{second}"

# return log message with time information
def logMessage():
    return f"SERVER LOG: {getTime()}"

# Get random 64 bit hexadecimal number
def getRandom():
    num = random.getrandbits(64)
    hex_num = format(num, '016x')
    return hex_num

def parseMessage(message):
    lines = message.split("\r\n")
    start_line = lines[0]
    method,target,version = start_line.split(" ")
    headers = {}
    for header in lines[1:]:
        if header == "": break #reached body
        hkey,hval = header.split(": ",1)
        headers[hkey] = hval
    return method, target, version, headers

def start_server(IP, PORT, SESSION_TIMEOUT):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            HTTPMessage = conn.recv(1024).decode("ascii")
            method, target, version, headers = parseMessage(HTTPMessage)
            
            if method == "POST" and target == "/":
                handle_post(headers, conn)
            elif method == "GET":
                handle_get(headers, conn, SESSION_TIMEOUT)
            else:
                s.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())

            conn.close()

def main():
    IP = sys.argv[1]
    PORT = int(sys.argv[2].strip(""))
    ACCOUNTS_FILE = sys.argv[3]
    SESSION_TIMEOUT = int(sys.argv[4])
    ROOT_DIRECTORY = sys.argv[5]

    start_server(IP, PORT, SESSION_TIMEOUT)

if __name__ == '__main__':
    main()