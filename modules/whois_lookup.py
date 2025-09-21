import socket

def whois_lookup(domain, console, server="whois.verisign-grs.com"):
    console.print(f"[*] Performing WHOIS lookup for {domain}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((server, 43))
        s.send((domain + "\r\n").encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        console.print(response.decode(errors="ignore"))
    except Exception as e:
        console.print(f"[red]WHOIS lookup failed: {e}[/red]")
