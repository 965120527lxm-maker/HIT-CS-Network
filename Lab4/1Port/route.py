import IP as ip
import socket as s

u_c=s.socket(s.AF_PACKET,s.SOCK_RAW,s.htons(ip.ETH_P_ALL))
my_ip=ip.get_local_ip()
if(my_ip!="192.168.10.3" and my_ip!="192.168.11.3"):
    print("You are not router!")
else:    
    my_port=ip.UDP_SRC_POR
    u_c.bind(("eth0",0))
    print(f"Your ip is:{my_ip}.\nThis is router,Listening on eth0 for raw Ethernet frames...")
    try:
        while True:
            udp_frame,src_addr=u_c.recvfrom(ip.BUFFER_SIZE)

            dest_mac,src_mac,eth_proto=ip.parse_ethernet_frame(udp_frame)
            if(eth_proto!=ip.ETH_P_IP):continue
            
            version, ip_hdr_len, ttl, proto, ip_checksum, src_ip, dst_ip, transport_data = ip.parse_ip_packet(udp_frame[14:])
            if proto != 17:  continue
            
            src_port, dst_port = ip.parse_tcp_udp(transport_data, 17)  # your function just reads first 4 bytes
            udp_header_len = 8
            udp_payload = transport_data[udp_header_len:]
            u_dict={
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

            print(f"[Recv]Frame from {u_dict['eth']['src_mac']}\nto{u_dict['eth']['dest_mac']},eth_proto={u_dict['eth']['eth_proto']}")
            print(f"{u_dict['ip']['src_ip']}")
            
            new_eth_hdr=ip.make_new_ethernet_hdr(dest_ip=dst_ip,src_ip=my_ip)
            u_c.send(new_eth_hdr+udp_frame[14:])
            print(f"[Forward]Datagram from ('{src_ip}',{src_port}) sent to ('{dst_ip}',{dst_port})")


            # send ip datagram
    except KeyboardInterrupt:
        print("[Quit]Close Router!")

# close
u_c.close()