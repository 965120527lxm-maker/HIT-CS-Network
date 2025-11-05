import IP as ip
import socket as s

u_c=s.socket(s.AF_PACKET,s.SOCK_RAW,s.htons(ip.ETH_P_IP))
src_ip=ip.get_local_ip()
print(f"Your ip is:{src_ip}")
src_port=ip.UDP_SRC_POR
u_c.bind(("eth0",0))

try:
    while True:
        net=input("Destination net 192.168.___.___:\n")
        host=input(f"Destination host 192.168.{net}.___:\n")
        dest_addr=(f"192.168.{net}.{host}",ip.UDP_SRC_POR) # to n10_host
        message=input(f"Message to {dest_addr}:\n")
        
        udp_frame=ip.make_udp_frame(src_ip,ip.UDP_SRC_POR,dest_addr[0],dest_addr[1],message.encode())
        # send ip datagram
        u_c.send(udp_frame)
        print(f"[Sent]Datagram from ('{src_ip}',{src_port}) sent to {dest_addr}")
except KeyboardInterrupt:
    print("[Quit]Close sender!")

# close
u_c.close()