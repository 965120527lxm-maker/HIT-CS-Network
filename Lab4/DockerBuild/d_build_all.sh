#!/bin/bash
# Create networks
docker network create --subnet=192.168.10.0/24 net10
docker network create --subnet=192.168.11.0/24 net11

# Create containers with correct IPs in the subnet range
docker run -itd --name net10_host1 --net net10 --ip 192.168.10.2 \
  --mac-address 9a:99:00:00:00:02 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=0 \
  lxmlab4docker  # Replace with your actual image

docker run -itd --name net10_host2 --net net10 --ip 192.168.10.3 \
  --mac-address 9a:99:00:00:00:03 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=1 \
  lxmlab4docker

docker run -itd --name net10_host3 --net net10 --ip 192.168.10.4 \
  --mac-address 9a:99:00:00:00:04 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=0 \
  lxmlab4docker

docker run -itd --name net10_host4 --net net10 --ip 192.168.10.5 \
  --mac-address 9a:99:00:00:00:04 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=0 \
  lxmlab4docker

docker run -itd --name net10_host5 --net net10 --ip 192.168.10.6 \
  --mac-address 9a:99:00:00:00:04 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=0 \
  lxmlab4docker

docker run -itd --name net11_host1 --net net11 --ip 192.168.11.2 \
  --mac-address 9a:99:00:00:01:02 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  --sysctl net.ipv4.ip_forward=0 \
  lxmlab4docker

# Connect the router (net10_host2) to net11 as well so that it forward the datagram from net11
docker network connect --ip 192.168.11.3 net11 net10_host2

# Wait for containers to be ready
sleep 5

# Add routes - FIXED: These should route between networks, not within same network
docker exec -it net10_host1 ip route add 192.168.11.0/24 via 192.168.10.3 dev eth0
docker exec -it net11_host1 ip route add 192.168.10.0/24 via 192.168.11.3 dev eth0
