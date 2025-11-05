import socket as s
import struct
import binascii
import string

BUFFER_SIZE=1518 
UDP_SRC_POR= 54321 
UDP_DST_POR= 54321

# send:
'''
1. send socket
2. make message bitarray into a UDP pkt ,then to a ip pkt, then a MAC
3. send to who?
'''

# forward
'''
1. every one send to the router,who hold one port?
2. the one parse the pkt,get the ip pkt,from the pkt konw who to send to
3. sendto((ip,ip))

? what is the ip? (mac,ip,port)?
now i know every one's 

3.TTL: time
'''

# how to wrap a mac , ip , and a UDP hdr



PROTOCOLS = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP'
}
def get_local_ip(target_ip="8.8.8.8"):
    """Find the local IP address used to reach a given target."""
    s1 =s.socket(s.AF_INET, s.SOCK_DGRAM)
    try:
        s1.connect((target_ip, 80))   # doesn’t actually send anything
        local_ip = s1.getsockname()[0]
    finally:
        s1.close()
    return local_ip

# route table
class route_entry:
    def __init__(self,dest:int,gateway:int,netmask:int,interface:str='eth0'):
        self.dest=dest
        self.gateway=gateway
        self.netmask=netmask
        self.interface=interface

ROUTE_TABLE_SIZE=100
route_table:list[route_entry]

def lookup_route(dest_ip)->route_entry|None:
    
    for route in (route_table):
        if (route.netmask & dest_ip )== (route.netmask & route.dest):
            return route
    return None

# Ethernet Frame
ETH_P_IP = 0x0800    # IP协议
ETH_P_ALL = 0x0003   # 所有协议
ether_table={
    "192.168.10.2": b"\x9a\x99\x00\x00\x00\x02", 
    "192.168.10.3": b"\x9a\x99\x00\x00\x00\x03",
    "192.168.10.4": b"\x9a\x99\x00\x00\x00\x04",
    "192.168.10.5": b"\x9a\x99\x00\x00\x00\x05",
    "192.168.10.6": b"\x9a\x99\x00\x00\x00\x06",
    "192.168.11.2": b"\x9a\x99\x00\x00\x01\x02",
    "192.168.11.3": b"\x9a\x99\x00\x00\x00\x03"
}

def make_ethernet_hdr(dest_ip,src_ip)->bytes:
    dest_mac=b"\x9a\x99\x00\x00\x00\x03"
    src_mac=ether_table[src_ip]
    
    eth_header=struct.pack("! 6s 6s H ",dest_mac,src_mac,ETH_P_IP)
    return eth_header

def make_new_ethernet_hdr(dest_ip,src_ip)->bytes:
    dest_mac=ether_table[dest_ip]
    src_mac=ether_table[src_ip]
    
    eth_header=struct.pack("! 6s 6s H ",dest_mac,src_mac,ETH_P_IP)
    return eth_header


def parse_ethernet_frame(data):
    # 以太网帧结构：目标MAC(6字节) + 源MAC(6字节) + 协议类型(2字节)
    dest_mac, src_mac, eth_proto = struct.unpack('! 6s 6s H', data[:14])
    return  src_mac,dest_mac,eth_proto


# Checksum
def checksum16(header:bytes)->int:

    if(len(header)%2 == 1):

        header+=b'\x00'

    s=0

    for i in range(0,len(header),2):

        word=(header[i]<<8)+header[i+1]

        s+=word

        s=(s& 0xFFFF)+(s>>16)



    return ~s & 0xFFFF

# Ip packet

import itertools
_ip_id_counter = itertools.count(0)
def next_ip_id():
    return next(_ip_id_counter) & 0xFFFF

def make_ip_hdr(src_ip,dest_ip,data,proto):
    version_IHL=0x45;ECN=0x00       ;Total_length=20+len(data)
    Identification=next_ip_id()     ;Flags=0b010;Fragment_offset=0 ;Flags_Frag=Flags<<13 | Fragment_offset
    TTL=0x40;Proto=17               ;Header_Checksum=0
    Src_ip  = s.inet_aton(src_ip)
    Dest_ip = s.inet_aton(dest_ip)

    ip_hdr=struct.pack("! B B H H H B B H 4s 4s",version_IHL,ECN,Total_length, 
                       Identification,Flags_Frag,
                       TTL,Proto,Header_Checksum,
                       Src_ip,
                       Dest_ip)    

    Header_Checksum=checksum16(ip_hdr)

    ip_hdr=struct.pack("! B B H H H B B H 4s 4s",version_IHL,ECN,Total_length, 
                       Identification,Flags_Frag,
                       TTL,Proto,Header_Checksum,
                       Src_ip,
                       Dest_ip)
    
    return ip_hdr

def parse_ip_packet(data):
    # 获取第一个字节中的版本号和头部长度
    version_header_length = data[0]
    version = version_header_length >> 4           # 右移4位得到版本号
    IHL=(version_header_length & 0b1111)    # 与1111相与得到头部长度（以4字节为单位）
    header_length = IHL*4
    
    ttl, proto,checksum, src_ip, target_ip = struct.unpack('! 8x B B H 4s 4s', data[:20])
    return (version,header_length, 
            ttl, proto, checksum ,
            s.inet_ntoa(src_ip), 
            s.inet_ntoa(target_ip),
            data[header_length:]
    )

# UDP
def make_udp_hdr(src_ip,src_port,dest_ip,dest_port,payload):
    src_ip=s.inet_aton(src_ip)
    dest_ip=s.inet_aton(dest_ip)
    
    udp_len=8+len(payload)
    checksum=0
    udp_hdr=struct.pack("!HHHH",
                        src_port,
                        dest_port,
                        udp_len,
                        checksum)
    pseudo_hdr=struct.pack("!4s 4s B B H",
                           src_ip,
                           dest_ip,
                           0,
                           17,
                           udp_len)
     
    checksum=checksum16(pseudo_hdr+udp_hdr+payload)
    udp_hdr=struct.pack("!HHHH",
                        src_port,
                        dest_port,
                        udp_len,
                        checksum)
    return udp_hdr

def parse_tcp_udp(data, protocol):
    """解析TCP/UDP头部
    格式说明：
    ! - 使用网络字节序
    H - 2字节无符号短整型（源端口）
    H - 2字节无符号短整型（目标端口）
    """
    if len(data) >= 4:
        # TCP/UDP头部都以源端口(2字节)和目标端口(2字节)开始
        src_port, dest_port = struct.unpack('! H H', data[:4])
        return src_port, dest_port
    return None, None

def parse_tcp_header(data):
    """解析TCP头部（示例）
    格式说明：
    ! - 使用网络字节序
    H - 源端口(2字节)
    H - 目标端口(2字节)
    I - 序列号(4字节)
    I - 确认号(4字节)
    H - 数据偏移(4位)+保留(6位)+标志位(6位)
    H - 窗口大小(2字节)
    """
    if len(data) >= 20:
        tcp_header = struct.unpack('! H H I I H H', data[:16])
        src_port = tcp_header[0]
        dst_port = tcp_header[1]
        sequence = tcp_header[2]
        acknowledgment = tcp_header[3]
        offset_flags = tcp_header[4]
        window_size = tcp_header[5]
        
        # 解析标志位
        data_offset = (offset_flags >> 12) * 4    # 右移12位获取数据偏移
        flags = offset_flags & 0x003F             # 与00111111相与获取标志位
        
        return {
            'source_port': src_port,
            'dest_port': dst_port,
            'sequence': sequence,
            'acknowledgment': acknowledgment,
            'data_offset': data_offset,
            'flags': flags,
            'window_size': window_size
        }
    return None

# MAKE/PARSE a FRAME
def make_udp_frame(src_ip:str,src_port:str,
                   dest_ip:str,dest_port:str,
                   data:str):
    udp_hdr=make_udp_hdr(src_ip=src_ip,src_port=src_port,
                         dest_ip=dest_ip,dest_port=dest_port,
                         payload=data)
    ip_payload=udp_hdr+data
    ip_hdr=make_ip_hdr(src_ip=src_ip,dest_ip=dest_ip,data=ip_payload,proto=17)
    ether_hdr=make_ethernet_hdr(src_ip=src_ip,dest_ip=dest_ip)
    return ether_hdr+ip_hdr+ip_payload

def parse_udp_frame(frame: bytes):
    # --- Ethernet layer (14 bytes) ---
    dest_mac, src_mac, eth_proto = parse_ethernet_frame(frame)
    if eth_proto != ETH_P_IP:
        raise ValueError(f"Not an IPv4 frame, eth_proto=0x{eth_proto:04x}")

    # --- IP layer ---
    # Pass everything after Ethernet header
    version, ip_hdr_len, ttl, proto, ip_checksum, src_ip, dst_ip, transport_data = parse_ip_packet(frame[14:])
    if proto != 17:  # 17 = UDP
        raise ValueError(f"Not a UDP packet, proto={proto}")

    # --- UDP layer ---
    # transport_data starts at UDP header already (because parse_ip_packet used header_length)
    src_port, dst_port = parse_tcp_udp(transport_data, 17)  # your function just reads first 4 bytes

    # UDP header is 8 bytes: src port (2) + dst port (2) + length (2) + checksum (2)
    udp_header_len = 8
    udp_payload = transport_data[udp_header_len:]

    return {
        "eth": {
            "dest_mac": dest_mac,
            "src_mac": src_mac,
            "eth_proto": eth_proto,
        },
        "ip": {
            "version": version,
            "header_length": ip_hdr_len,
            "ttl": ttl,
            "proto": proto,
            "checksum": ip_checksum,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
        },
        "udp": {
            "src_port": src_port,
            "dst_port": dst_port,
            "payload": udp_payload,
        }
    }


# 创建原始套接字，监听所有协议
# i_s = s.socket(s.AF_PACKET, s.SOCK_RAW, s.htons(ETH_P_ALL))

# try:
#     print("[Start] 监听所有网络接口的流量...")
#     print("按 Ctrl+C 停止")
    
#     while True:
#         raw_data, ret_ip = i_s.recvfrom(BUF_SIZE)
        
#         # 解析以太网帧
#         dest_mac, src_mac, eth_proto = parse_ethernet_frame(raw_data)
        
#         # 只处理IP包
#         if eth_proto == ETH_P_IP:
#             # 解析IP包
#             ip_data = raw_data[14:]  # 跳过以太网头部
#             version, header_length, ttl, proto, src_ip, dest_ip, transport_data = parse_ip_packet(ip_data)
            
#             # 获取传输层信息（TCP/UDP端口）
#             src_port, dest_port = parse_tcp_udp(transport_data, proto)
            
#             print("\n" + "="*50)
#             print(f"协议: {PROTOCOLS.get(proto, str(proto))}")
#             print(f"源地址: {src_ip}:{src_port if src_port else 'N/A'}")
#             print(f"目标地址: {dest_ip}:{dest_port if dest_port else 'N/A'}")
#             if proto == 6:  # TCP
#                 print("TCP连接")
#             elif proto == 17:  # UDP
#                 print("UDP数据报")
                
# except KeyboardInterrupt:
#     print("\n[Quit] 停止监听")
# finally:
#     i_s.close()

        