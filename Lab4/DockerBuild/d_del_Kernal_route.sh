docker start \
net10_host1 \
net10_host2 \
net10_host3 \
net10_host4 \
net10_host5 \
net11_host1

for i in {1..5}; do
  docker exec -it net10_host$i ip route add 192.168.11.0/24 via 192.168.10.3 dev eth0
done
docker exec -it net11_host1 ip route add 192.168.10.0/24 via 192.168.11.3 dev eth0

# to verify
for i in {1..5}; do
  echo "=== net10_host$i ==="
  docker exec net10_host$i ip route show
done
echo "=== net10_host1 ==="
docker exec net10_host1 ip route show
