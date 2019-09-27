import os
import socket
import subprocess

host = '127.0.0.1'
port = 10000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print(f'SSH Service Running on {host}:{port}')
    conn, addr = s.accept()
    with conn:
        print('Client Connected with IP :', addr)
        while True:
            cmd = conn.recv(1024).decode('utf8')
            if not cmd:
                break
            if cmd == 'exit':
                break
            print('Executing : ', cmd)
            if cmd.strip().startswith('cd'):
                try:
                    if len(cmd.split()) == 1:
                        cmd += ' ~'
                    path = cmd.split()[1]
                    if path.startswith('~'):
                        user = subprocess.getoutput('whoami')
                        path = path.replace('~', f'/home/{user}')
                    os.chdir(path)
                    conn.send(f'Changed to {path}'.encode('utf8'))
                except FileNotFoundError as e:
                    conn.send(e.strerror.encode('utf8'))
            else:
                output = subprocess.getoutput(cmd)
                if output:
                    conn.send(output.encode('utf8'))
                else:
                    conn.send(f'executed {cmd}'.encode('utf8'))
