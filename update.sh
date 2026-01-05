#! /usr/bin/bash
# python3 -m pip install --upgrade build
# python3 -m pip install --upgrade twine

echo "Building last version"
if python3 -m build; then
    echo "Uploading last version to PyPI"
    if var=`df -h | twine upload dist/* --verbose` ; then
        copy=${var:0:-1}
        len=${#copy}
        for((i=$len-1;i>=0;i--)); do rev="$rev${copy:$i:1}"; done
        string=$rev
        substring="/"
        prefix="${string%%$substring*}"
        if [ "$prefix" != "$string" ]; then index=${#prefix}
        else index=-1
        fi
        version=${var:${#var}-$index-1:-1}
    else
        echo "Couldn't upload to PyPI. Maybe you forgot to change the version number?"
        exit 1
    fi
else
    echo "Couldn't build the package"
    exit 1
fi

while :
do
    s=`df -h | pip index versions python-imager`
    if [[ $s == *$version* ]] ; then
        break
    else
        echo "Waiting (python-imager==$version not yet uploaded)"
        sleep 3
    fi
done
pip install python-imager==$version
rm dist/*
rmdir dist
exit 0