make clean;v=$(make bump_version);echo $v ;make dist && twine upload dist/* && \
git commit pyproject.toml package.json jgtml/__init__.py -m v$v &>/dev/null  && \
git tag $v &>/dev/null && \
pip install -e .
git push &>/dev/null 
git push --tags &>/dev/null

