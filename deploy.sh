#!/bin/bash

# System params
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURR_DIR="${DIR##*/}"

# Pulling
source ${DIR}/venv/bin/activate

echo -e "\033[92m\nGit pull... Press enter to continue...\033[0m" & read
git pull

echo -e "\033[92m\nSet users rights\033[0m" & read
sudo chmod 0777 ${DIR}/data -R
sudo chmod 0777 ${DIR}/media -R
sudo chmod 0777 ${DIR}/static -R
chown www-data /var/log/${CURR_DIR}/ -R
sudo chmod 0777 /var/log/${CURR_DIR}/ -R

echo -e "\033[92m\nSync database... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py migrate
echo -e " "
python ${DIR}/src/manage.py syncprefs
echo -e " "
python ${DIR}/src/manage.py synctpls
echo -e " "
python ${DIR}/src/manage.py syncmodules

echo -e "\033[92m\nSync static files... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py collectstatic

echo -e "\033[92m\nRestart supervisor... Press enter to continue...\033[0m" & read
supervisorctl restart www.mandarin.one
supervisorctl restart www.mandarin.one_celery

deactivate