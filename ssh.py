import socket

import sys
if len(sys.argv) != 2:
    print('Provide Arguments')
    print('Syntax : ssh.py [address]')
    exit(-1)
host = sys.argv[1]
port = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((host, port))
    except ConnectionRefusedError as e:
        print(f'Can not Connect to {host}')
        exit(-1)
    s.send('whoami'.encode('utf8'))
    user = s.recv(1024).decode('utf8')
    s.send('hostname'.encode('utf8'))
    hostname = s.recv(1024).decode('utf8')
    s.send('cd ~'.encode('utf8'))
    s.recv(1024)
    while True:
        s.send('pwd'.encode('utf8'))
        pwd = s.recv(1024).decode('utf8')
        pwd = pwd.replace(f'/home/{user}', '~')
        msg = input(f'{user}@{hostname}:{pwd}$ ')
        s.send(bytes(msg, 'utf8'))
        if msg == 'exit':
            break
        print(s.recv(4096).decode('utf8'))
