
DIR_BASE=$(cd $(dirname $0); pwd)
echo "DIR_BASE: $DIR_BASE"
dist_path=$(realpath $(du -a dist|grep whl|awk '{print $2}'))
