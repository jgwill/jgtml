make clean;v=$(make bump_version);make dist && twine upload dist/* && git tag $v ;git push --tags &>/dev/null && git push &>/dev/null 
