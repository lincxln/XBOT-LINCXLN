export LANG=C.UTF-8

echo -e "\nChecking Dependencies...\n"
echo -e "\nMemeriksa Dependensi...\n"

if command -v python3 >/dev/null 2>&1 ; then
    echo -e "python3 found (python ada) "
    echo -e "version: $(python3 -V)"
else
    echo -e "python not found (python tidak ada) "
    if [ "$(command -v pkg)" != "" ]; then
        arr+=(python ) #termux python3 is in python
    else
        arr+=(python3 )
    fi
fi

sleep 1

if command -v wget >/dev/null 2>&1 ; then
    echo -e "\nwget found (wget ada)\n"
else
    echo -e "\nwget not found (wget tidak ada)\n"
    arr+=(wget )
fi

DEPENDENCIES=${arr[@]}
sleep 1

if [ ! -z "$DEPENDENCIES" ]; then
    echo -e "\nInstalling required dependencies\n"
    echo -e "\nMenginstal dependensi yang diperlukan\n"
    sleep 1

    if [ "$(command -v pkg)" != "" ]; then # termux
        pkg install "$DEPENDENCIES" -y

    elif [ "$(command -v apt-get)" != "" ]; then # debian
        sudo apt-get install "$DEPENDENCIES" -y

    elif [ "$(command -v pacman)" != "" ]; then # arch
        sudo pacman -S "$DEPENDENCIES" -y

# Free to PR to add others
    else
        echo -e "\nDistro not supported \nInstall this packages yourself: $DEPENDENCIES\n"
        echo -e "\nDistro tidak didukung \nInstal paket ini sendiri: $DEPENDENCIES\n"
    fi

else
    echo -e "\nDependencies have been installed. \nContinuing to install python packages(PyPI)\n"
    echo -e "\nDependensi telah diinstal. \nMelanjutkan menginstal paket python(PyPI)\n"
    sleep 1
fi

echo -e "\nUpgrading python pip\n"
echo -e "\nMemutakhirkan python pip\n"
pip3 install --upgrade pip setuptools
echo -e "\nInstalling telethon...\n"
echo -e "\nMenginstall telethon...\n"
pip3 install telethon
sleep 2

if [ ! -e string_session.py ]; then
    echo -e "\nDownloading string_session.py\n"
    echo -e "\nMengunduh string_session.py\n"
    wget https://raw.githubusercontent.com/lincxln/XBOT-LINCXLN/alpha/string_session.py

    echo -e "\nRunning script...\n"
    echo -e "\nMenjalankan script\n"
    sleep 1
    python3 string_session.py
else
    echo -e "\nstring_session.py detected... \nrunning file\n"
    echo -e "\nstring_session.py Terdeteksi... \nMenjalankan File"
    sleep 1
    python3 string_session.py
fi

echo -e "Do you want to cleanup your file?"
echo -e "\nApakah Anda ingin membersihkan file Anda?"
echo -e "[1] cleanup: this delete string_session.py and this file"
echo -e "[2] exit"
echo -ne "\nEnter your choice[1-2]: "
read choice
if [ "$choice" = "1" ]; then
    echo -e "Cleanup: removing file"
    rm -f string_session.py Getstring.sh
elif [ "$choice" = "2" ]; then
    exit
fi
