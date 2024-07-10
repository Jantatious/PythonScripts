"""
Quick little Python script to help convert MAC addresses into vendor-specific
formats. 

Requires the MAC address and format to be supplied when the script is called
(for now)
"""

import re
import sys 

# Regex that matches valid MAC characters
MAC_REGEX = re.compile(r"[A-Fa-f0-9]")

# Dictionary for with supported MAC address formats
MAC_FORMATS = {"cisco": "cccc.cccc.cccc", 
               "linux": "cc:cc:cc:cc:cc:cc", 
               "windows": "CC-CC-CC-CC-CC-CC"}

def mac_format(mac_string: str) -> str:
    replace_chars: list = ["-", ":", ".", ";"]

    for i in replace_chars: 
        mac_string = mac_string.replace(i, "")
        print(mac_string)

    mac_string = mac_string.lower()
    return mac_string

def extract_mac(address: str) -> list[str]:
    address_chars = re.findall(MAC_REGEX, address)
    address_chars = "".join(address_chars)
    # print(address_chars)
    return address_chars

def validate_mac(address: str) -> int:
    if len(address) != 12:
        print("The supplied MAC address is invalid. Please try again.")
        return 0
    return 1

def validate_args() -> int:
    # Checks that the proper amount of arguments were supplied. 
    if len(sys.argv) < 3:
        print("""
ERROR: Incorrect number of arguments supplied. Two arguments are required.
- The MAC address
- The desired format
Please check your inputs and try again.
              """)
        return 0
    return 1

def format_linux(address: list, separator: str = ":", to_lower: int = 1) -> str:
    """Also used for converting to Windows format. It just changes separator"""
    addr_str = ""
    for i in range(0, len(address), 2):
        addr_str += address[i:i+2]
        if i + 2 < len(address):
            addr_str += separator
    if to_lower:
        return addr_str.lower()
    else:
        return addr_str.upper()

def format_cisco(address: list, separator:str = ".") ->str:
    addr_str = ""
    for i in range(0, len(address), 4):
        addr_str += address[i:i+4]
        if i + 4 < len(address):
            addr_str += separator
    return addr_str.lower()

if __name__ == "__main__":
    if not validate_args():
        quit()

    mac_address: list[str] = extract_mac(sys.argv[1])

    if not validate_mac(mac_address):
        quit()

    # print(mac_address)

    if sys.argv[2].lower() == "linux":
        print(format_linux(mac_address))
    elif sys.argv[2].lower() == "windows" or sys.argv[2].lower() == "win":
        print(format_linux(mac_address, separator="-", to_lower=0))
    elif sys.argv[2].lower() == "cisco":
        print(format_cisco(mac_address))
    else:
        print(f"{sys.argv[2]} is not recognized. Please try again.")
