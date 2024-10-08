#git commit package.json pyproject.toml jgtml/__init__.py -m bump &>/dev/null
sleep 2
make bump_jgtpy
#. pre-build.sh

. scripts/version-patcher.sh
cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
git commit . -m "v$cversion" && git tag "$cversion" && git push --tags && git push 

make dist && twine upload dist/* && echo "pip install -U jgtml" && echo "pip install -U jgtml==$cversion"
