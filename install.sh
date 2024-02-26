#!/bin/sh
#
# THIS SCRIPT WILL INSTALL THE GNORDVPN APP SYSTEM WIDE
# THE SCRIPT MUST BE RUN WITH SUDO
#
# It will create a startup shell script named gnordvpn in /usr/bin,
# the app will be placed in /usr/share/gnordvpn-sprokkel78
# The .desktop file will be placed in /usr/share/applications/ as com.sprokkel78.gnordvpn.desktop

mkdir -p /usr/share/glanscan-sprokkel78
cp -r ./* /usr/share/glanscan-sprokkel78/
echo "#!/bin/sh" > /usr/bin/glanscan
echo "cd /usr/share/glanscan-sprokkel78" >> /usr/bin/glanscan
echo "python3 ./glanscan.py" >> /usr/bin/glanscan
cp ./glanscan.desktop /usr/share/applications/com.sprokkel78.glanscan.desktop
chmod 755 /usr/bin/glanscan
chmod 644 /usr/share/glanscan-sprokkel78/*
