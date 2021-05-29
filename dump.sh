#!/bin/bash

# System params
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Dump db
source ${DIR}/venv/bin/activate
echo -e "\033[92m\nClean up... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py thumbnail clear_delete_all
echo -e "\033[92m\nMake db dump... Press enter to continue...\033[0m" & read
python ${DIR}/src/manage.py dumpdata pages preferences shop website --indent 4 > ${DIR}/data/db.json
deactivate

# Dump media
cd ${DIR}
tar -pczf ${DIR}/data/media.tar.gz --exclude ./media/cache ./media --totals
sudo chmod 0777 ${DIR}/data -R

# End
echo -e ""