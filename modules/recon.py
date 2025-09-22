import socket
import requests
import math


def dns_lookup(domain, console):
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[green]{domain} → {ip}[/green]")
        return ip
    except socket.gaierror:
        console.print(f"[red]Could not resolve {domain}[/red]")
        return None


def geo_point_from_data(data):

    try:
        lat = float(data.get("lat"))
        lon = float(data.get("lon"))
    except Exception:
        return None

    label = data.get("query") or ""
    small = data.get("City" or data.get("country")) or data.get("org" or "")
    if small and data.get("country"):
        small = f"{small}, {data.get('country')}"
    elif not small and data.get("country"):
        small = f"{data.get('country')}"
    return {"lat": lat, "lon": lon, "label": label, "small": small}

def draw_ascii_map(points, width=79, height=20, title=None, marker="*"):


    grid = [[" " for _ in range(width)] for _ in range(height)]

    meridian_step = 30

    for lon in range(-180, 181, meridian_step):
        x = int(round((lon + 180) / 360 * (width - 1)))
        for y in range(height):

            grid[y][x] = "|" if grid[y][x] == " " else grid[y][x]

    parallel_step = 15
    for lat in range(90, -91, -parallel_step):
        y = int(round((90 - lat) / 180 * (height - 1)))
        for x in range(width):
            grid[y][x] = "-" if grid[y][x] == " " else grid[y][x]

        if lat == 0:
            for x in range(width):
                grid[y][x] = "="


    placed = []
    for pt in points:
        try:
            lat = float(pt["lat"])
            lon = float(pt["lon"])
        except Exception:
            continue

        if lon < -180: lon = -180
        if lon > 180: lon = 180
        if lat > 90: lat = 90
        x = int(round((lon + 180) / 360 * (width - 1)))
        y = int(round((90 - lat) / 180 * (height - 1)))


        if grid[y][x] != " " and grid[y][x] != "|" and grid[y][x] != "-" and grid[y][x] != "=":
            # find nearby free cell in radius 2
            found = False
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] in (" ", "|", "-", "="):
                        y, x = ny, nx
                        found = True
                        break
                if found:
                    break
        grid[y][x] = marker
        placed.append((x, y, pt))

    if title:
        print(f" {title}")
    # print top longitudes header (simple)
    lon_labels = []
    for lon in range(-180, 181, 60):
        x = int(round((lon + 180) / 360 * (width - 1)))
        lon_labels.append((x, str(lon)))
    # print grid
    for row in grid:
        print("".join(row))


    # Print longitude ruler
    ruler = [" "]*width
    for x, label in lon_labels:
        lab = label
        for i,ch in enumerate(lab):
            if x + i < width:
                ruler[x + i] = ch
    print("".join(ruler))



    if placed:
        print()
        print(" Plotted points:")
        for i, (x, y, pt) in enumerate(placed, 1):
            lbl = pt.get("label") or pt.get("hint") or f"{pt.get('lat')},{pt.get('lon')}"
            hint = pt.get("hint") or ""
            print(f"  {i}. {marker} @ ({pt['lat']:.4f}, {pt['lon']:.4f})  {lbl}  {hint}")
    else:
        print("\n No points plotted.")


def geo_ip(query, console=None, return_data=False):


    url = f"http://ip-api.com/json/{query}"

    try:
        req = requests.get(url, timeout=5)
        data = req.json()
    except Exception as e:
        if console:
            console.print(f"[red]Error fetching IP geolocation data: {e}[/red]")
        else:
            print(f"[red]Error fetching IP geolocation data: {e}[/red]")
        return None

    out = {
        "query": data.get("query"),
        "country": data.get("country"),
        "countryCode": data.get("countryCode"),
        "region": data.get("regionName") or data.get("region"),
        "city": data.get("city"),
        "zip": data.get("zip"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "timezone": data.get("timezone"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "as": data.get("as"),
    }

    if console:
        console.print(f"[bold]IP Geolocation for [/bold][cyan]{out['query']}[/cyan]:")

        for k,v in out.items():
            console.print(f"[magenta]{k}[/magenta]: {v}")
    else:
        for k,v in out.items():
            print(f"[magenta]{k}[/magenta]: {v}")


    if return_data:
        return out
    return out