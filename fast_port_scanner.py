import socket
import sys
import time
import queue
import threading
from termcolor import cprint
import keyboard

usage = "Usage - python3 port_scanner.py TARGET START_PORT END_PORT Threads"

ban = """\n
:::::::::   ::::::::  ::::::::: :::::::::::       ::::::::   ::::::::      :::     ::::    ::: ::::    ::: :::::::::: :::::::::  
:+:    :+: :+:    :+: :+:    :+:    :+:          :+:    :+: :+:    :+:   :+: :+:   :+:+:   :+: :+:+:   :+: :+:        :+:    :+: 
+:+    +:+ +:+    +:+ +:+    +:+    +:+          +:+        +:+         +:+   +:+  :+:+:+  +:+ :+:+:+  +:+ +:+        +:+    +:+ 
+#++:++#+  +#+    +:+ +#++:++#:     +#+          +#++:++#++ +#+        +#++:++#++: +#+ +:+ +#+ +#+ +:+ +#+ +#++:++#   +#++:++#:  
+#+        +#+    +#+ +#+    +#+    +#+                 +#+ +#+        +#+     +#+ +#+  +#+#+# +#+  +#+#+# +#+        +#+    +#+ 
#+#        #+#    #+# #+#    #+#    #+#          #+#    #+# #+#    #+# #+#     #+# #+#   #+#+# #+#   #+#+# #+#        #+#    #+# 
###         ########  ###    ###    ###           ########   ########  ###     ### ###    #### ###    #### ########## ###    ### \n
"""
cprint(ban, "light_green")

if len(sys.argv) != 5:
    cprint(usage, "red", attrs=["bold"])
    sys.exit()

target = sys.argv[1]

try:
    start_port = int(sys.argv[2])
except ValueError:
    cprint("[*] Invalid START_PORT. Please provide an integer value.", "red")
    sys.exit()

if start_port < 0 or start_port > 65535:
    cprint("[*] START_PORT must be in the range 0-65535.", "red")
    sys.exit()


try:
    end_port = int(sys.argv[3])
except ValueError:
    cprint("[*] Invalid END_PORT. Please provide an integer value.", "red")
    sys.exit()

if end_port < 0 or end_port > 65535:
    cprint("[*] END_PORT must be in the range 0-65535.", "red")
    sys.exit()

if start_port > end_port:
    cprint("[*] START_PORT must be less than or equal to END_PORT.", "red")
    sys.exit()


try:
    thread_no = int(sys.argv[4])
except ValueError:
    cprint("[*] Invalid number of Threads. Please provide an integer value.", "red")
    sys.exit()

if thread_no <= 0:
    cprint("[*] Number of Threads must be greater than 0.", "red")
    sys.exit()


res = "\n[+] Result: "
result = "\nPORT\tSTATE\tSERVICE\n"

try:
    target = socket.gethostbyname(target)
except socket.gaierror:
    print("[*] Host resolution failed")
    sys.exit()

print(f"Scanning target: {target}")


def get_banner(port, s):
    try:
        s.settimeout(2)
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return "Unknown"


def scan_port():
    global result
    while True:
        port = q.get()
        if port is None:
            break
        print(f"Scanning for port {port}")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            conn = s.connect_ex((target, port))
            if not conn:
                banner = get_banner(port, s)
                banner = ''.join(banner.splitlines())
                result += f"{port}\tOPEN\t{banner}\n"
            s.close()
        except:
            pass
        q.task_done()


q = queue.Queue()
threads = []

start_time = time.time()

for _ in range(thread_no):
    t = threading.Thread(target=scan_port)
    t.start()
    threads.append(t)

for port in range(start_port, end_port + 1):
    q.put(port)

q.join()

for _ in range(thread_no):
    q.put(None)
for t in threads:
    t.join()

end_time = time.time()
cprint(res, "red", attrs=["blink"])
cprint(result, "cyan")
print(f"Time taken for scan: {end_time - start_time:.2f} seconds")

attempts = 0
while attempts < 3:
    cprint("[+] Do you want the results to be output in a file? [Y/N]", "cyan")
    while True:
        if keyboard.is_pressed('Y') or keyboard.is_pressed('y'):
            with open("ports.txt", "w") as file:
                file.write(f"Port scan results for target: {target}\n")
                file.write(result)
            cprint("[+] Written to file ports.txt.", "red")
            break
        elif keyboard.is_pressed('N') or keyboard.is_pressed('n'):
            cprint("[+] Exiting the program.", "red")
            sys.exit()
    break