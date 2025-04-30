#!/bin/bash

URL="https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"

function ok() {
    echo "[OK]"
}

if [[ ${UID} != "0" ]];
then
    echo "Invalid user ${UID}, required root..."
    exit 0
fi


#mkdir -p /opt/jennt/DoMRevInject/data && echo "[OK]" || echo "[ERROR]"
cd data/

printf "[?] Remove older versino if exists...\t\t"
rm -f /tmp/firefox.tar.xz
rm -rf /tmp/firefox.tar
#rm -rf firefox-portable
rm -rf firefox-*
ok

printf "[?] Downloading firefox...\t\t"
wget -q -O /tmp/firefox.tar.xz "${URL}" 2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"
printf "[?] Decompress firefox...\t\t"
tar -Jxvf /tmp/firefox.tar.xz  2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"
#ls firefox

printf "[?] Move firefox to firefox portable...\t\t"
mv firefox firefox-portable
ok

cd ..
python3 domrevinject_pro.py
rm -rf data/firefox-portable
mv data/firefox-injector.zip firefox-injector.zip

echo ""
ls firefox-injector.zip && printf "\n\nYeah!! Happy Hacking!!\n\npython3 run.py\n\n"
#rm -f firefox.tar.bz2

printf "[?] make venv and install python requirements...\t\t"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


echo "source .venv/bin/activate"
echo "python3 run.py"


