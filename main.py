import struct
import socket
from colorama import Fore, Back, Style
import textwrap


TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

ETHER_TYPE = {
    'IPv4': 8
}

INTERNET_PROTOCOL = {
    'ICMP': 1,
    'TCP': 6
}
    

def main():
    conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_packet(raw_data)

        print_with_color('Ethernet frame: ', Fore.YELLOW)
        print(TAB_1 + 'Destination: {}; Source: {}; Protocol: {}'.format(dest_mac, src_mac, eth_proto))

        if eth_proto == ETHER_TYPE['IPv4']:
            version, header_length, ttl, proto, src, target, data = ipv4_packet(data)
            print_with_color(TAB_1 + 'IPv4 packet:', Fore.RED)
            print(TAB_2 + 'Version: {}; Header_length: {}; Time to live: {}'.format(version, header_length, ttl))
            print(TAB_2 + 'Protocol: {}; Source: {}; Target: {}'.format(proto, src, target))

            if proto == INTERNET_PROTOCOL['ICMP']:
                icmp_type, code, checksum, data = icmp_packet(data)
                print_with_color(TAB_2 + 'ICMP packet:', Fore.GREEN)
                print(TAB_3 + 'Type: {}; Code: {}; Checksum: {}'.format(icmp_type, code, checksum))
                print_with_color(TAB_3 + 'Data:', Fore.CYAN)
                print_raw(data, indent='\t\t\t\t')

            elif proto == INTERNET_PROTOCOL['TCP']:
                src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = tcp_segment(data)
                print_with_color(TAB_2 + 'TCP segment:', Fore.GREEN)
                print(TAB_2 + 'Source port: {}; Destination port: {}; Sequence: {}; Acknowledgement: {}'.format(src_port, dest_port, sequence, acknowledgement))
                print(TAB_3 + 'Flags: URG={}, ACK={}, PSH={}, RST={}, SYN={}, FIN={}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print_with_color(TAB_3 + 'Data:', Fore.CYAN)
                print_raw(data, indent='\t\t\t\t')


# Prints text with color
def print_with_color(text, color=None):
    if color:
        print(color + text + Style.RESET_ALL)
    else:
        print(text)


# Prints raw data in hexadecimal
def print_raw(data, width=80, indent='', color=None):
    text = ' '.join([f'{byte:02X}' for byte in data])
    lines = textwrap.wrap(text, width=width, initial_indent=indent, subsequent_indent=indent)
    for line in lines:
        print_with_color(line, color=color)


# Unpacks an Ethernet frame
def ethernet_packet(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]


# Returns a more readable MAC address format
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


# Unpacks a IPv4 packet (see 'assets/ipv4-header.jpg')
def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    # The IHL value is multiplied by 4, since its value represents the header length  in 32-bit words (4 bytes), not bytes
    header_length = (version_header_length & 0b00001111) * 4

    # 8x: skip 8 bytes
    # B: unsigned char (1 byte) -> int
    # 4s: C string -> string
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])

    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]


# Returns a more readable IPv4 address format ([192, 168, 1, 1] --> '192.168.1.1')
def ipv4(addr):
    return '.'.join(map(str, addr))


# Unpacks an ICMP packet
def icmp_packet(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:]


# Unpacks an TCP segment
def tcp_segment(data):
    src_port, dest_port, sequence, acknowledgement, offset_reserved_flag = struct.unpack('! H H L L H', data[:14])
    offset = (offset_reserved_flag >> 12) * 4   # offset's value is in words (4 bytes)
    flag_urg = (offset_reserved_flag & 32) >> 5
    flag_ack = (offset_reserved_flag & 16) >> 4
    flag_psh = (offset_reserved_flag & 8) >> 3
    flag_rst = (offset_reserved_flag & 4) >> 2
    flag_syn = (offset_reserved_flag & 2) >> 1
    flag_fin = offset_reserved_flag & 1
    return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]



if __name__ == '__main__':
    main()