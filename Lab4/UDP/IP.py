import socket as s
import struct
import binascii
import string
import ipaddress
BUF_SIZE = 4096
# 定义以太网协议号
ETH_P_IP = 0x0800    # IP协议
ETH_P_ALL = 0x0003   # 所有协议

# 定义协议映射
PROTOCOLS = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP'
}

class route_entry:
    def __init__(self,dest:int,gateway:int,netmask:int,interface:str='eth0'):
        self.dest=dest
        self.gateway=gateway
        self.netmask=netmask
        self.interface=interface

ROUTE_TABLE_SIZE=100
route_table:list[route_entry]

# route_table is global
def lookup_route(dest_ip)->route_entry|None:
    
    for route in (route_table):
        if (route.netmask & dest_ip )== (route.netmask & route.dest):
            return route
    return None





def parse_ethernet_frame(data):
    """解析以太网帧
    格式说明：
    ! - 使用网络字节序（大端序）
    6s - 6字节的字符串（MAC地址）
    6s - 6字节的字符串（MAC地址）
    H - 2字节的无符号短整型（协议类型）
    """
    # 以太网帧结构：目标MAC(6字节) + 源MAC(6字节) + 协议类型(2字节)
    dest_mac, src_mac, eth_proto = struct.unpack('! 6s 6s H', data[:14])
    return binascii.hexlify(dest_mac).decode(), binascii.hexlify(src_mac).decode(), eth_proto

def parse_ip_packet(data):
    """解析IP包头
    格式说明：
    ! - 使用网络字节序
    8x - 跳过8字节（版本、服务类型、总长度、标识、标志等）
    B - 1字节无符号整数（TTL）
    B - 1字节无符号整数（协议）
    2x - 跳过2字节（校验和）
    4s - 4字节字符串（源IP）
    4s - 4字节字符串（目标IP）
    """
    # 获取第一个字节中的版本号和头部长度
    version_header_length = data[0]
    version = version_header_length >> 4           # 右移4位得到版本号
    header_length = (version_header_length & 15) * 4   # 与1111相与得到头部长度（以4字节为单位）
    
    
    # IP头部结构：版本(4位) + 头部长度(4位) + 服务类型(1字节) + 总长度(2字节) + ...
    ttl, proto, src_ip, target_ip = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, s.inet_ntoa(src_ip), s.inet_ntoa(target_ip), data[header_length:]

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

# 创建原始套接字，监听所有协议
# i_s = s.socket(s.AF_PACKET, s.SOCK_RAW, s.htons(ETH_P_ALL))

# try:
#     print("[Start] 监听所有网络接口的流量...")
#     print("按 Ctrl+C 停止")
    
#     while True:
#         raw_data, ret_addr = i_s.recvfrom(BUF_SIZE)
        
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

        