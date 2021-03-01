import socket
import sys

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        host = 'localhost'
        port = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        year = sys.argv[1]
        state = sys.argv[2]
        print('sender:', [year, state])
        s.send(str(year+','+state).encode('utf-8'))
        server_data = s.recv(4096)
        print('recv:', str(server_data, 'utf-8'))
