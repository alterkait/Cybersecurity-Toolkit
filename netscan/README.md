This Python script scans your local network and lists the IP addresses, hostnames (if available), and MAC addresses of the devices connected to it. It uses the Address Resolution Protocol (ARP) to find active devices on the network. The script is compatible with Windows, Linux, and macOS.

## How it Works

1. The script starts by getting the local IP address of the machine running the script.
2. It then extracts the subnet from the local IP address.
3. A broadcast ping is sent to the local network to update the ARP table.
4. The script retrieves the ARP table, which calls the 'arp' command provided by the operating system.
5. The ARP table output is parsed to extract IP addresses, hostnames, and MAC addresses of the devices on the network.
6. Finally, the script prints the information about each device in a readable format.

## Usage

Ensure Python 3.x is installed. 
Also Ensure socket, re, subprocess Python libraries are installed:

```
pip install socket
pip install re
pip install subprocess
```

## Disclaimer

Use this script responsibly and only on networks for which you have proper authorisation. Scanning networks without proper authorisation may be against your network's policy or even illegal in some jurisdictions.
