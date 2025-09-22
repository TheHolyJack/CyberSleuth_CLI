# CyberSleuth

CyberSleuth is a Windows-friendly CLI cybersecurity toolset that provides various network reconnaissance and security assessment tools.

## Features

- **Network Scanning**
  - Ping sweep for host discovery
  - Port scanning with multi-threading support
  - ARP scanning for local network device discovery
  

- **Domain Information**
  - DNS lookup functionality
  - WHOIS domain lookup
  - HTTP headers analysis
  

- **Geographical Information**
  - GeoIP lookup
  - ASCII map visualization of geographical data

## Installation

Requires Python 3.8 or higher.

Install from source:

```bash
git clone https://github.com/TheHolyJack/CyberSleuth
cd cybersleuth
pip install .
```

## Dependencies

- certifi
- idna
- rich
- scapy
- requests

## Usage

After installation, you can run CyberSleuth from the command line:

```bash
cybersleuth [command] [options]
```

## Features in Detail

### Network Scanning
- **Ping Sweep**: Scan a subnet to discover active hosts
- **Port Scan**: Perform TCP port scanning on specified hosts
- **ARP Scan**: Discover devices on your local network using ARP

### Domain Information
- **WHOIS Lookup**: Retrieve domain registration information
- **HTTP Headers**: Analyze HTTP headers of web servers

### Logging
- Supports both CSV and JSON output formats
- Timestamps for all operations
- Structured data logging

## Development

This project is structured as a Python package and uses:
- setuptools for packaging
- rich for console output
- threading for concurrent operations

## License

You may use as you please.

## Contributing

Make a pull request, we'll see what we can do. 
## Notes

- This tool is designed to be Windows-friendly while maintaining compatibility with other operating systems
- Use responsibly and in accordance with applicable laws and regulations
- Some features may require administrative privileges