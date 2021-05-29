#!/bin/bash

# System params
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURR_DIR="${DIR##*/}"
PROJECT_NAME=${CURR_DIR//[-.]/_}

# Install packages
echo -e "\033[92m\nInstalling system packages... Press enter to continue...\033[0m" & read
sudo apt-get install build-essential libjpeg-dev libpq-dev python3-pip python3-dev python3-venv python3-setuptools uwsgi-plugin-python3 gettext curl redis-server

# Python virtualenv setup
echo -e "\033[92m\nInstalling python vitrualenv... Press enter to continue...\033[0m" & read
rm -rf ${DIR}/venv
python3 -m venv ${DIR}/venv
chmod +x ${DIR}/venv/bin/activate

echo -e "\033[92m\nInstalling python packages... Press enter to continue...\033[0m" & read
source ${DIR}/venv/bin/activate
pip install --upgrade setuptools virtualenv requests wheel
pip install -r ${DIR}/requirements.txt
deactivate

# Create dirs
echo -e "\033[92m\nCreate dirs... Press enter to continue...\033[0m" & read
mkdir -p ${DIR}/data
mkdir -p ${DIR}/static
mkdir -p ${DIR}/media
mkdir -p ${DIR}/media/public/
mkdir -p ${DIR}/media/thumbs/
mkdir -p ${DIR}/media/public/root/
sudo mkdir -p /var/log/${CURR_DIR}/

# Delete Mysql DB
export PGPASSWORD='postgres';
echo -e "\033[92m\nDelete old database... Press enter to continue...\033[0m" & read
psql -h localhost -U postgres -c "drop database if exists www_mandarin_one "
echo -e "\033[92m\nCreate new database... Press enter to continue...\033[0m" & read
psql -h localhost -U postgres -c "create database www_mandarin_one with owner \"postgres\" encoding='utf8' template template0"

# Manage.py commands
source ${DIR}/venv/bin/activate
echo -e "\033[92m\nDjango migrate... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py migrate
echo -e "\033[92m\nDjango collectstatic... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py collectstatic
if [ -f ${DIR}/data/db.json ]; then
    if [[ -f ${DIR}/data/media.tar.gz ]]; then
        echo -e "\033[92m\nLoad test data... Press enter to continue...\033[0m" & read
        tar -xvf ${DIR}/data/media.tar.gz
        python ${DIR}/src/manage.py loaddata ${DIR}/data/db.json
    fi
fi
echo -e "\033[92m\nDjango syncprefs... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py syncprefs
echo -e "\033[92m\nDjango synctpls... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py synctpls
echo -e "\033[92m\nDjango syncmodules... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py syncmodules
deactivate

# User rights
echo -e "\033[92m\nSet users rights\033[0m" & read
sudo chmod 0777 ${DIR}/data -R
sudo chmod 0777 ${DIR}/media -R
sudo chmod 0777 ${DIR}/static -R
sudo chmod 0777 /var/log/${CURR_DIR}/ -R
sudo chown www-data /var/log/${CURR_DIR}/ -R

# End
echo -e ""
