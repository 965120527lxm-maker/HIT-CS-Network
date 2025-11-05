filename=$1
net=$2
host=$3

net_host="net${net}_host${host}"
path=${4:-/lab}

docker cp ${filename} ${net_host}:${path}
