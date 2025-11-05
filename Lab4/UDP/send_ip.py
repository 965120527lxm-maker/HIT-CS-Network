import IP as ip
import socket as s
import struct

sockfd:int
port=12345
dest_addr=("192.168.10.3",port) # to n10_h2

try:
    while True:
        message=input("Put in the message you want to send,Ctrl+C if want to QUIT:\n")
        #  create udp socket 
        u_c=s.socket(s.AF_INET,s.SOCK_DGRAM,s.IPPROTO_UDP)
        # u_c.bind("192.168.10.3",port)

        # send ip datagram
        u_c.sendto(message.encode(),dest_addr)
        print(f"[Sent]Datagram sent to {dest_addr}")
except KeyboardInterrupt:
    print("[Quit]Close sender!")

# close
u_c.close()

