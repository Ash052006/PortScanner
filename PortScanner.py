import socket
from IPy import IP   # Library used to validate whether input is a proper IP address


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

        print('[+] Port ' + str(port) + ' is Open')

    except:
        # Q: When does this block execute?
        # A: When sock.connect() throws an exception.
        # This usually happens when:
        # - Port is closed
        # - Host is unreachable
        # - Connection times out

        print('[-] Port ' + str(port) + ' is Closed')


# ===== MAIN PROGRAM =====

ipaddress = input('[+] Enter target to scan: ')
# User enters either:
# - An IP address (e.g., 192.168.1.1)
# - A domain name (e.g., google.com)

converted_ip = check_ip(ipaddress)
# Q: Why store converted_ip?
# A: Because if user enters a domain name,
# it gets converted into an IP before scanning.


for port in range(75, 85):
    scan_port(converted_ip, port)
    # This loop scans ports 75 to 84 (85 is excluded).
    # For each port, scan_port() attempts a TCP connection.