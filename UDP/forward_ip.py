import socket as s
import IP as ip
buffer:str
src_port=12345
dest_port=54321

# create UDP socket
u_s=s.socket(s.AF_INET,s.SOCK_DGRAM,s.IPPROTO_UDP)
u_s.bind(("0.0.0.0",src_port))
print("[Start]Forwarding node start!")

try:
    while True:
        # receive datagram
        buffer,ret_addr=u_s.recvfrom(ip.BUF_SIZE)
        print(f"[Receive]Datagram received:{buffer} from:{ret_addr}")

        # Update dest_addr
        u_s.sendto(buffer,("192.168.10.4",dest_port))
        print(f"[Forward]Datagram forwarded to (\'192.168.10.4\',dest_port)")
except KeyboardInterrupt:
    print("[Quit]Forwarder Closed!")
u_s.close()

