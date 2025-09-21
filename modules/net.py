import subprocess
import ipaddress
import threading
from queue import Queue

def ping_host(ip, console, results):
    try:
        result = subprocess.run(["ping", "-n", "1", "-w", "1000", str(ip)],
                                stdout=subprocess.DEVNULL)
        status = "UP" if result.returncode == 0 else "DOWN"
        if status == "UP":
            console.print(f"[green]{ip}[/green]")
        else:
            console.print(f"[red]{ip}[/red]")
        results.append({"IP": str(ip), "Status": status})
    except Exception:
        results.append({"IP": str(ip), "Status": "ERROR"})

def ping_sweep(subnet, console):
    net = ipaddress.ip_network(subnet, strict=False)
    console.print(f"[*] Starting ping sweep on {subnet}...")
    results = []
    q = Queue()
    for ip in net.hosts():
        q.put(ip)

    def worker():
        while not q.empty():
            ip = q.get()
            ping_host(ip, console, results)
            q.task_done()

    for _ in range(50):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()
    console.print("[*] Ping sweep completed.")
    return results
