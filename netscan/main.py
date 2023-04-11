import os
import re 
import socket
import subprocess

#get IP address of machine running the script
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        print(f"Error: {e}")

#Extract subnet from the local IP address        
def get_subnet(ip_address):
    subnet = '.'.join(ip_address.split('.')[:-1])
    return subnet

def send_broadcast_ping(subnet):
    broadcast_ip = f"{subnet}.255"
    try:
        if os.name == 'nt':  # For Windows
            subprocess.check_output(['ping', '-n', '1', '-w', '1000', broadcast_ip],
                                    stderr=subprocess.DEVNULL, universal_newlines=True)
        else:  # For Linux and macOS
            subprocess.check_output(['ping', '-c', '1', '-W', '1', '-b', broadcast_ip],
                                    stderr=subprocess.DEVNULL, universal_newlines=True)
    except subprocess.CalledProcessError:
        pass

#Get ARP table provided by the OS
def get_arp_table():
    if os.name == 'nt':  # For Windows
        arp_command = 'arp -a'
    else:  # For Linux and macOS
        arp_command = 'arp -n'
        
    output = subprocess.check_output(arp_command, shell=True, universal_newlines=True)
    return output

#Parse ARP table output to extract IP addresses, hostnames, MAC addresses
def parse_arp_table(arp_output, subnet):
    pattern = re.compile(rf"({subnet}\.[0-9]{{1,3}}).*?(([0-9A-Fa-f]{{2}}[:-]){{5}}([0-9A-Fa-f]{{2}}))")
    devices = []

    for match in pattern.finditer(arp_output):
        ip_address = match.group(1)
        mac_address = match.group(2)
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.error:
            hostname = None
        devices.append((ip_address, hostname, mac_address))

    return devices

if __name__ == "__main__":
    local_ip = get_local_ip()
    subnet = get_subnet(local_ip)
    print(f"Scanning network: {subnet}.0/24")

    send_broadcast_ping(subnet)
    arp_output = get_arp_table()
    devices = parse_arp_table(arp_output, subnet)
    for device in devices:
        print(f"IP: {device[0]}, Hostname: {device[1] if device[1] else 'Unknown'}, MAC: {device[2]}")
