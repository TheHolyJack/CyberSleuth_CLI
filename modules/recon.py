import socket

def dns_lookup(domain, console):
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[green]{domain} → {ip}[/green]")
        return ip
    except socket.gaierror:
        console.print(f"[red]Could not resolve {domain}[/red]")
        return None
