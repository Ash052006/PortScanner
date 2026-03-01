"""
TCP Port Scanner

Author: Aishwary

Description:
A basic TCP port scanner that:
- Accepts single or multiple targets
- Validates IP addresses
- Resolves domain names to IP addresses
- Scans ports 1–499
- Attempts banner grabbing on open ports

For educational purposes only.
"""

import socket
from IPy import IP   # Library used to validate whether input is a proper IP address


def scan(target):
    """
    Initiates scanning process for a given target.

    Parameters:
    target (str): IP address or domain name

    Process:
    - Validates or resolves the target
    - Iterates through ports 1–499
    - Calls scan_port() for each port
    """
    converted_ip = check_ip(target)
    print('\n' + '[-_0 Scanning Target]' + str(target))

    for port in range(1, 500):
        scan_port(converted_ip, port)


def check_ip(ip):
    """
    This function checks whether the user input is:
    1) Already a valid IP address
    2) A domain name that needs conversion to IP

    If it is a valid IP → return as it is
    If not → resolve the domain to IP using DNS
    """
    try:
        IP(ip)
        # Q: Why use IP(ip)?
        # A: It verifies whether the given string is a valid IP address.
        # If valid → no exception occurs.
        # If invalid → it raises a ValueError and jumps to except.

        return ip
        # If no exception happened, it means input was already a valid IP.

    except:
        # Q: When does Python enter except?
        # A: When IP(ip) throws an exception (meaning input is not a valid IP).

        return socket.gethostbyname(ip)
        # Q: What does gethostbyname() do?
        # A: It converts a domain name (e.g., google.com) into its IP address.
        # This process is called DNS resolution.


def get_banner(s):
    """
    Attempts to receive service banner from an open port.

    Parameters:
    s (socket): Active socket connection

    Returns:
    bytes: Raw banner data (max 1024 bytes)
    """
    return s.recv(1024)


def scan_port(ipaddress, port):
    """
    This function attempts to connect to a given IP address and port.

    If connection succeeds → port is Open.
    If connection fails → exception occurs → port is Closed.
    """
    try:
        sock = socket.socket()
        # Q: Why create socket first?
        # A: Because settimeout() and connect() are methods of the socket object.
        # We must create the socket object before configuring or using it.

        sock.settimeout(0.5)
        # Q: Why place settimeout() here?
        # A: Timeout must be set BEFORE calling connect().
        # It defines how long connect() should wait before giving up.
        # If placed after connect(), it would not affect that connection attempt.
        # If placed before socket creation, it would cause an error (object doesn't exist).

        sock.connect((ipaddress, port))
        # Q: How does Python know whether to print Open or Closed?
        # A: If connect() succeeds → no exception → execution continues.
        #    If connect() fails (port closed / timeout / firewall) →
        #    it raises an exception and jumps to except block.

        try:
            banner = get_banner(sock)
            print('[+] Open Port ' + str(port) + ' : ' + str(banner.decode().strip('\n')))
        except:
            print('[+] Port ' + str(port))

    except:
        # Q: When does this block execute?
        # A: When sock.connect() throws an exception.
        # This usually happens when:
        # - Port is closed
        # - Host is unreachable
        # - Connection times out

        # print('[-] Port ' + str(port) + ' is Closed')
        pass


# ===== MAIN PROGRAM =====

# User enters either:
# - An IP address (e.g., 192.168.1.1)
# - A domain name (e.g., google.com)

if __name__ == '__main__':
    targets = input('[+] Enter Target/s To Scan(split multiple targets with ,): ')

    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))
    else:
        scan(targets)

# End of Program