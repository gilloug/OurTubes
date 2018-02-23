#!/bin/bash

echo "Please execute this script as root."
echo "Required and NOT INSTALLED WITH THIS SCRIPT :"
echo "\t- mysql"
echo "\t- pip3 (python3-pip)"
echo "Press y to continue, any other key to stop :"

read -n 1 var
echo ""
if [ -z $var ]
then
    exit 0
fi

if [ $var != 'y' ]
then
    exit 0
fi

pip3 install google-api-python-client
pip3 install flask
pip3 install flask-mysql
pip3 install flask_cors

echo "Enter your root mysql password bellow"
mysql -u root -p < database.sql

echo "Installation complete, launch server with ./index.py"
