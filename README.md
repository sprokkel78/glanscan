glanscan-sprokkel78

A graphical user interface in PyGTK for use with the nmap binary for scanning your lan and performing portscans on Ubuntu and other Linux distro's. 
It requires Python3.10 or higher, Pip, Venv and the PyGTK apps, it also relies on gnome-terminal for performing portscans.
Developed and tested on Ubuntu 23.10. 

Installation on Ubuntu 23.10

1. $sudo apt install python3 python3-dev python3-pip python3-venv
2. $sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
3. $sudo apt install gnome-terminal

Added 'install.sh' script for system-wide installation.
- The startup shell script will be /usr/bin/glanscan
- The application is installed in /usr/share/glanscan-sprokkel78
- The .desktop file is placed in /usr/share/applications/com.sprokkel78.glanscan.desktop

Added 'uninstall.sh' script for system-wide uninstallation.
- This will delete /usr/bin/glanscan and /usr/share/glanscan-sprokkel78,
  This will also remove /usr/share/applications/com.sprokkel78.glanscan.desktop
  
Check https://www.github.com/sprokkel78/glanscan for contributing, development features and pre-releases.

Funding: Paypal email: sprokkel78.bart@gmail.com
