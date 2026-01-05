#! /usr/bin/bash
# python3 -m pip install --upgrade build twine

echo "Building last version"
if v=`df -h | python3 -m build`
then echo "Uploading last version to PyPI"
    if v=`df -h | twine upload dist/*`
    then echo Successfully uploaded to PyPI
    else echo "Couldn't upload to PyPI. Maybe you forgot to change the version number?"
    fi
else echo "Couldn't build the package"
fi
rm dist/*; rmdir dist;
echo Waiting for python-imager to be available
sleep 10
python -m pip install --upgrade python-imager
echo "python -m pip install --upgrade python-imager"