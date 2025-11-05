## To do
### 实验内容

(1)  使用虚拟机实现多主机间的UDP数据报收发及转发

利用虚拟机搭建实验环境，掌握Linux下的Socket网络编程。 

> 选做1：改进程序，示例程序只实现了一个数据包（携带1条消息）的发、转、收过程，要求实现每条消息由**控制台输入**，并且**不限制发送消息的数目**。 

(2)  基于单网口主机的IP数据转发及收发 

在局域网中，模拟IP数据报的路由转发过程。通过原始套接字实现了完整的数据封
装过程，**实现了UDP头部、IP头部、MAC帧头部的构造**。 

> 选做2：扩展实验的**网络规模**，由原始方案中3台主机增加到不少于5台主机，共同完成IP数据报转发及收发过程，要求**采用转发表**改进示例程序，增加程序通用性。 

(3)  基于双网口主机的路由转发 

构造了**静态路由表**，并实现了**不同子网间的IP数据报查表转发**过程。 

> 选做3：通过完善**路由表**，改进示例程序实现**双向传输**。

In fact , use sendto() will wrap a frame to my_frame.

so how to transfer?

## Ip UDP
![alt text](image/image.png)
![alt text](image/UDP.png)

## Docker
### to build a docker,write a dockerfile

```dockerfile
docker network create --subnet=192.168.0.0/24 net0
docker network create --subnet=192.168.1.0/24 net1
docker run -itd --name net0_host1 --net net0 --ip 192.168.0.2 --mac-address 9a:99:00:00:00:02 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker run -itd --name net0_host2 --net net0 --ip 192.168.0.3 --mac-address 9a:99:00:00:00:03 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker run -itd --name net0_host3 --net net0 --ip 192.168.0.4 --mac-address 9a:99:00:00:00:04 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker run -itd --name net0_host4 --net net0 --ip 192.168.0.5 --mac-address 9a:99:00:00:00:05 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker run -itd --name net0_host5 --net net0 --ip 192.168.0.6 --mac-address 9a:99:00:00:00:06 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker run -itd --name net1_host1 --net net1 --ip 192.168.1.2 --mac-address 9a:99:00:00:01:02 --cap-add=NET_RAW --cap-add=NET_ADMIN --sysctl net.ipv4.ip_forward=0 lab4docker
docker network connect --ip 192.168.1.3 net1 net0_host2
                       			   	def ip		//define mac			//cap_add,capability add ,GET raw datagram   //no forward           
docker exec -it net0_host1 ip route add 192.168.1.0/24 via 192.168.0.3 dev eth0
docker exec -it net1_host1 ip route add 192.168.0.0/24 via 192.168.1.3 dev eth0
```


### daily docker operation:
1. vm , log in  :docker exec -it [hostname] bash
2. docker cp [filename] [hostname:path]: from host to vm 
3. docker ps
4. docker start [hostname]: open the hosts.
5. docker exec -it [hostname] [file_to_exec]

### appendies
to gene a docker :

1. dockerfile /*Important!!!!!!!!!!!!!!!!!!!!!!*/-> docker 

2. build //make a mirrow

done:

- env , docker is able to compile and run a 

todo : 
- 1.read lab file, and write

## Python 

### Bytes array
```py
b"ABC"				#ASCII bytes for 'A''B''C'. str are unicode text 
b"\x41\x42\x43"		#same as above , in hexadecimal 
```
Bytes are the raw form of data, Before it is decoded.

```py
data=text.encode("utf-8") 	-> 	from utf to ASCII bytes array;
text=data.decode("utf-8") 	-> 	from bytes to utf string
```

for a trial:
```py 
#bitwise operators
'''
& 
~ 
^ 
<< 
>>
'''
a=0b1100
b=0b0011

print(bin(a|b))
print(bin(a&b))
print(bin(a^b))


mask=0b1110
print(bin((a>>1)&mask)) #get the bit you want


# bytes and str
'''
string - bytes

- string ->bytes
b'A'
"A".encode()
b"\x40"
bytes.fromhex("40")

- bytes  ->string
b"\x40".decode()

'''
mac_bytes = b"\x9a\x99\x00\x00\x00\x02"
print(mac_bytes)

print(mac_bytes.hex()) # to string

print(bytes.fromhex("9a9900000002"))


print(b'A')
print('A'.encode())        #b'\x41',   
print(b"\x41".decode())    #0x41->A
print(bytes.fromhex('41')) #bytes,the true bit: 0x41,b'\x41'
#first look at its type 
binary= 0b11001010
decimal=202
hexodecimal=0xCA


# packing and unpacking
import struct

''' Pack 3 unsigned bytes '''
packed = struct.pack("!BBB", 1, 2, 3)
print(packed)  # b'\x01\x02\x03'

''' Unpack them back '''
a, b, c = struct.unpack("!BBB", packed)
print(a, b, c)  # 1 2 3
```

| Operation    | Example                          | Output     |
| ------------ | -------------------------------- | ---------- |
| Int → binary | `bin(10)`                        | `'0b1010'` |
| Int → hex    | `hex(255)`                       | `'0xff'`   |
| Hex → int    | `int("ff", 16)`                  | `255`      |
| Binary → int | `int("1010", 2)`                 | `10`       |
| Int → bytes  | `(255).to_bytes(1, 'big')`       | `b'\xff'`  |
| Bytes → int  | `int.from_bytes(b'\xff', 'big')` | `255`      |


