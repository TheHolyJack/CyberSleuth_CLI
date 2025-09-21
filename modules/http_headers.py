import requests

def grab_headers(url, console):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        console.print(f"[*] Fetching headers for {url}...")
        response = requests.get(url, timeout=5)
        for k, v in response.headers.items():
            console.print(f"[cyan]{k}[/cyan]: {v}")
    except Exception as e:
        console.print(f"[red]Failed to fetch headers: {e}[/red]")
