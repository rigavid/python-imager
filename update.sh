#! /usr/bin/bash
# python3 -m pip install --upgrade build twine

Version() {
    while read l; do
    if [[ $l == *"version"* ]]; then
        prf="${l%%\"*}"
        if [ "$prf" != "$l" ]
        then ind=${#prf}
        else ind=-1 ; fi
        version=${l:$ind+1:-1}
    fi done < pyproject.toml
    if $verbose; then echo "python-imager==$version"
    else echo $version ; fi
}

Help() { # Display Help
   echo "Install the python-imager update and publish it to PyPI"
   echo
   echo "Syntax: $0 [-l|v|V|h]"
   echo "options:"
   echo "l, --local   Install the update without publishing to PyPI"
   echo "v, --verbose Verbose"
   echo "V, --version Print python-imager's version"
   echo "h, --help    Print this Help"
   echo
}

TEMP=$(getopt -o hvVl --long help,verbose,version,local -- "$@")
eval set -- "$TEMP"

verbose=false
local=false
while true; do
  case "$1" in
      -h | --help ) Help; exit 0 ;;
      -v | --verbose ) verbose=true; shift ;;
      -V | --version ) Version; exit 0 ;;
      -l | --local ) local=true; break ;;
      * ) break ;;
  esac
done


if $local
then
    echo Local installation
    echo "Building last version"
    if v=`df -h | python3 -m build`
        then echo "Last version builded"
        else
            echo "Couldn't build the package"
            exit 2
    fi
else
    echo "Building last version"
    if v=`df -h | python3 -m build`
    then echo "Uploading last version to PyPI"
        if v=`df -h | twine upload dist/*`
        then echo Successfully uploaded to PyPI
        else echo "Couldn't upload to PyPI. Maybe you forgot to change the version number?"
        fi
    else echo "Couldn't build the package" ; fi
fi

ls dist | tail -$N | while read file
do if [[ ${file:${#file}-7} == ".tar.gz" ]]
then pip install dist/$file
fi done
rm dist/*; rmdir dist;
exit 0