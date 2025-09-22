import socket
import threading
from queue import Queue

def scan_port(host, port, console, results):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        if sock.connect_ex((host, port)) == 0:
            console.print(f"[green]Port {port} OPEN[/green]")
            results.append({"Port": port, "Status": "OPEN"})
        else:
            console.print(f"[red]Port {port} closed[/red]")
            results.append({"Port": port, "Status": "CLOSED"})
        sock.close()
    except Exception as e:
        results.append({"Port": port, "Status": f"ERROR | {e}"})

def port_scan(host, ports, console):
    console.print(f"[*] Starting port scan on {host}...")
    results = []
    q = Queue()
    for port in ports:
        q.put(port)

    def worker():
        while not q.empty():
            port = q.get()
            scan_port(host, port, console, results)
            q.task_done()

    for _ in range(min(50, len(ports))):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()
    console.print("[*] Port scan completed.")
    return results
