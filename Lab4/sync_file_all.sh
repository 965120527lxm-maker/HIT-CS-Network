filename=$1
path=${2:-/lab}

docker start \
net10_host1 \
net10_host2 \
net10_host3 \
net10_host4 \
net10_host5 \
net11_host1

for i in {1..5};do 
   docker cp ${filename} net10_host$i:${path}
done
docker cp ${filename} net11_host1:${path}

