make clean;v=$(make bump_version);echo $v ;make dist && twine upload dist/* && \
git add pyproject.toml package.json jgtml/__init__.py && \
git commit pyproject.toml package.json jgtml/__init__.py -m v$v  && \
git tag $v
git push &>/dev/null 
git push --tags &>/dev/null

