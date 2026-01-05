#! /usr/bin/bash
# python3 -m pip install --upgrade build twine

echo "Building last version"
if python3 -m build; then
    echo "Uploading last version to PyPI"
    if var=`df -h | twine upload dist/*` ; then
        c=${var:0:-1}; len=${#c}; for((i=$len-1;i>=0;i--)); do rev="$rev${c:$i:1}"; done
        s=$rev; ss="/"; p="${s%%$ss*}"; if [ "$p" != "$s" ]; then index=${#p}; else index=-1; fi
        version=${var:${#var}-$index-1:-1}
    else echo "Couldn't upload to PyPI. Maybe you forgot to change the version number?"; exit 1; fi
else echo "Couldn't build the package"; exit 1; fi
rm dist/*; rmdir dist
while :; do
    s=`df -h | pip index versions python-imager`; if [[ $s == *$version* ]] ; then break
    else echo "Waiting (python-imager==$version not yet uploaded)"; sleep 3; fi
done; pip install --upgrade python-imager; exit 0