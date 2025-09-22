import argparse
from modules import net, scan, recon, arp, whois_lookup, http_headers
from utils import Logger
from rich.console import Console
from rich.table import Table

console = Console()

def print_table(title, columns, data):
    """
    Print a rich table.
    :param title: Table title
    :param columns: List of column names
    :param data: List of dictionaries with keys matching columns
    """
    table = Table(title=title, show_lines=True)
    for col in columns:
        table.add_column(col, style="cyan", no_wrap=True)
    for row in data:
        table.add_row(*(str(row.get(col, "")) for col in columns))
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description='CyberSleuth CLI Toolset')

    subparsers = parser.add_subparsers(dest='command')

    # PING SWEEP ARGUMENTS
    ping_parser = subparsers.add_parser('ping', help="Ping sweep a subnet.")
    ping_parser.add_argument('--subnet', required=True, help="Target Subnet, e.g. 192.168.1.0/24")

    # PORT SCAN ARGUMENTS
    scan_parser = subparsers.add_parser("scan", help="Scan ports on a host")
    scan_parser.add_argument('--host', required=True, help="Target Host")
    scan_parser.add_argument('--ports', default="22,80,443",  help="Comma Separated ports. e.g. 22,80,443 (default)")

    # DNS LOOKUP ARGUMENTS
    dns_parser = subparsers.add_parser("dns", help="DNS lookup for a domain.")
    dns_parser.add_argument('--domain', help="Domain to query")

    # ARP SCAN ARGUMENTS
    arp_parser = subparsers.add_parser("arp", help="ARP lookup.")

    # WHOIS ARGUMENTS
    whois_parser = subparsers.add_parser("whois", help="Whois lookup.")
    whois_parser.add_argument('--domain', help="Domain to query", required=True)

    # HTTP HEADER ARGUMENTS
    http_parser = subparsers.add_parser("headers", help="Grab HTTP Headers")
    http_parser.add_argument('--domain', help="Domain to query", required=True)


    # IP GEOLOCATION ARGUMENTS
    geo_parser = subparsers.add_parser("geo", help="IP Geolocation (Not always accurate)")
    geo_parser.add_argument('--ip', required=True, help="IP for the query.")

    geo_parser.add_argument("--ascii-map", action="store_true", help="Show ASCII Map point of the IP address.")


    # LOGGING ARGUMENTS
    parser.add_argument('--log-csv', help="Write logs to a CSV file.")
    parser.add_argument('--log-json', help="Write logs to a JSON file.")

    args = parser.parse_args()

    import socket, ipaddress
    if args.command == "ping" and not args.subnet:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network = ipaddress.ip_network(local_ip + "/24", strict=False)
        args.subnet = str(network)



    # TODO: Make this a switch or something, yandere dev level if statement incoming
    # Dispatch commands
    if args.command == "ping":
        results = net.ping_sweep(args.subnet, console)
        if results:
            print_table(f"Ping Sweep Results ({args.subnet})", ["IP", "Status"], results)
        if args.log_csv:
            Logger.log_csv(args.log_csv, results, headers=["IP", "Status"])
        if args.log_json:
            Logger.log_json(args.log_json, results)

    elif args.command == "scan":
        ports = [int(p) for p in args.ports.split(",")]
        results = scan.port_scan(args.host, ports, console)
        if results:
            print_table(f"Port Scan Results ({args.host})", ["Port", "Status"], results)
        if args.log_csv:
            Logger.log_csv(args.log_csv, results, headers=["Port", "Status"])
        if args.log_json:
            Logger.log_json(args.log_json, results)

    elif args.command == "dns":
        ip = recon.dns_lookup(args.domain, console)
        if ip:
            print_table("DNS Lookup", ["Domain", "IP"], [{"Domain": args.domain, "IP": ip}])
        if args.log_csv:
            Logger.log_csv(args.log_csv, [{"Domain": args.domain, "IP": ip}], headers=["Domain", "IP"])
        if args.log_json:
            Logger.log_json(args.log_json, [{"Domain": args.domain, "IP": ip}])

    elif args.command == "arp":
        results = arp.arp_scan(console)
        if results:
            print_table("ARP Scan Results", ["IP", "MAC"], results)
        if args.log_csv:
            Logger.log_csv(args.log_csv, results, headers=["IP", "MAC"])
        if args.log_json:
            Logger.log_json(args.log_json, results)

    elif args.command == "whois":
        whois_lookup.whois_lookup(args.domain, console)

    elif args.command == "headers":
        http_headers.grab_headers(args.url, console)

    elif args.command == "geo":
        data = recon.geo_ip(args.ip, console=console, return_data=True)

        if data:

            table_data = [{"Failed": k, "Value": v} for k,v in data.items()]
            print_table(f"GeoIP: {args.ip}", ["Field", 'Value'], table_data)

            if args.ascii_map:
                pt = recon.geo_point_from_data(data)
                if pt:
                    recon.draw_ascii_map([pt], width=79, height=20, title=f"Geoip: {args.ip}")

            if args.log_csv:
                Logger.log_csv(args.log_csv, [data], headers=list(data.keys()))
            if args.log_json:
                Logger.log_json(args.log_json, [data])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
