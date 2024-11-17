glanscan-sprokkel78

A graphical user interface in PyGTK4 for use with the nmap binary for scanning your lan and performing portscans
on Ubuntu and other Linux distro's. 
It requires Python3.10 and the PyGTK apps, it also relies on gnome-terminal for performing portscans. 
Developed on Fedora41 and tested on Ubuntu 24.04.

Runs out of the	box after default installation of Fedora or Ubuntu.

![Screenshot](https://github.com/sprokkel78/glanscan/blob/develop/screenshots/glanscan-1.png)

Installation on Fedora41 and Ubuntu 24.04
    $sudo dnf|apt install gnome-terminal nmap
    $git clone https://github.com/sprokkel78/glanscan.git
    $cd glanscan
    $python3 ./glanscan.py

For System-Wide Installation, run:

    $sudo ./install.sh

Then start with:

    $glanscan
    or by clicking the application icon.

Added 'install.sh' script for system-wide installation.

    The startup shell script will be /usr/bin/glanscan
    The application is installed in /usr/share/glanscan-sprokkel78
    The .desktop file is placed in /usr/share/applications/com.sprokkel78.glanscan.desktop

Added 'uninstall.sh' script for system-wide uninstallation.

    This will delete /usr/bin/glanscan and /usr/share/glanscan-sprokkel78, This will also remove /usr/share/applications/com.sprokkel78.glanscan.desktop

Check https://www.github.com/sprokkel78/glanscan for contributing, development features and pre-releases.

Check https://pypi.org/project/glanscan-sprokkel78/ for the full python package.

Funding: Paypal email: sprokkel78.bart@gmail.com
