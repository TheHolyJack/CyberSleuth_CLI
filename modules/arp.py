import subprocess
import re

def arp_scan(console):
    console.print("[*] Scanning local network for devices via ARP...")
    results = []
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        lines = output.splitlines()
        for line in lines:
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([\w-]+)", line)
            if match:
                ip, mac = match.groups()
                console.print(f"[green]IP={ip}[/green], MAC={mac}")
                results.append({"IP": ip, "MAC": mac})
    except Exception as e:
        console.print(f"[red]Error during ARP scan: {e}[/red]")
    return results
