import socket as s
import IP as ip
buffer:str
src_port=12345
dest_port=54321
try:
    while True:
        # create UDP socket
        u_s=s.socket(s.AF_INET,s.SOCK_DGRAM,s.IPPROTO_UDP)
        u_s.bind(("0.0.0.0",dest_port))
        print(f"[Start]Listening at src_port {dest_port}")

        # receive datagram
        buffer,ret_addr=u_s.recvfrom(ip.BUF_SIZE)
        print(f"[Recv]Datagram received:{buffer} from:{ret_addr}")
except KeyboardInterrupt:
    print("[Quit]Receiver Closed!")
u_s.close()




