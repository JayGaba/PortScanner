import socket, sys
import time

usage = "Usage - python3 port_scanner.py TARGET START_PORT END_PORT"

print("*" * 20)
print("Python Port Scanner")
print("*" * 20)

target = sys.argv[1]
target = socket.gethostbyname(target)
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

start_time = time.time()

if not target or not str(start_port) or not end_port:
    print(usage)
    exit()

for port in range(start_port, end_port + 1):
    print(f"[*] Scanning for port {port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    conn = s.connect_ex((target, port))
    if not conn:
        print(f"[*] Port {port} is open")

end_time = time.time()
print(f"Time taken for scan: {end_time - start_time:.2f} seconds")
