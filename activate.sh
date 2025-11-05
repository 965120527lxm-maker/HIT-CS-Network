net=$1
host=$2

net_host="net${net}_host${host}"
docker start ${net_host}
echo "Log in ${net_host}"
docker exec -it "${net_host}" bash


