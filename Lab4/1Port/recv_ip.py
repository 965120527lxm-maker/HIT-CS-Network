import IP as ip
import socket as s

u_c=s.socket(s.AF_INET,s.SOCK_DGRAM)
my_ip=ip.get_local_ip()
print(f"Your ip is:{my_ip}")
my_port=ip.UDP_SRC_POR
u_c.bind(('',my_port))

try:
    while True:
        udp_frame,src_addr=u_c.recvfrom(ip.BUFFER_SIZE)

        print(f"[Recv]Datagram from {src_addr},payload:")
        print(udp_frame)

        # send ip datagram
except KeyboardInterrupt:
    print("[Quit]Close Receiver!")

# close
u_c.close()