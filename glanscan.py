import os.path
import socket
import subprocess
import sys
import gi
import threading

gi.require_version('Gtk', '4.0')
gi.require_version("Gdk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, GLib
from time import sleep

# VERSION = 1.0.4
ver = "1.0.4"


# GLOBAL VARIABLES
global thread
global thread_started

tbuffer = Gtk.TextBuffer()
entry_host = Gtk.Entry()
entry_iprange = Gtk.Entry()
button_ipscan = Gtk.Button(label="IP-Scan")
button_ipscan_stop = Gtk.Button(label="Stop")
statusbar = Gtk.Label(label="")


# STARTUP CHECKS

# CHECK IF GLANSCAN.PY IS ALREADY RUNNING

print("Check if gLanScan is already running. please wait.")
status = subprocess.Popen("ps ax | grep \"python3 ./glanscan.py\" | grep -v \"grep\"",
                          shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
rcstat = status.wait()
out = status.communicate()
test = out[0].split("\n")

if len(test) > 1:
    if "glanscan.py" in test[1]:
        print("gLanScan is already running. (EXIT)" + test[0])
        sys.exit(0)
else:
    print("Running gLanScan. (CONTINUE)")


# CHECK IF THE NMAP COMMANDLINE TOOL IS INSTALLED

file = "/usr/bin/nmap"
if os.path.exists(file):
    print("Found the nmap binary. (CONTINUE)")
else:
    print("Can't find the nmap binary. It should be in /usr/bin/ (EXIT)")
    sys.exit(0)


# DEF - THREAD CLASS
class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        #while not self._stop_event.is_set():
        print("Thread is running...")

        global tbuffer
        global entry_iprange

        iprange = entry_iprange.get_text()
        if iprange != "" and ";" not in iprange:
            txt = ""
            txt = txt + "\n\tScan Report: "

            status = subprocess.Popen("pkexec /usr/bin/nmap -P " + iprange + " | grep -E \"report|open\"",
                                          shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
            out = status.communicate()
            txt_split = out[0].split("\n")
            x = 0
            y = 0
            while (x < len(txt_split)):
                if "report" in txt_split[x]:
                    y = y + 1
                    txt = txt + "\n"
                txt = txt + "\n\t" + txt_split[x]
                x = x + 1

            txt = txt + "\n\tHosts Up: " + str(y) + "\n"
            GLib.idle_add(tbuffer.set_text, txt)

        print("Thread stopped.")
        statusbar.set_text("  Done.")
        entry_iprange.set_sensitive(1)
        button_ipscan.set_sensitive(1)
        sleep(3)


def stop_thread(thread):
    global thread_started
    thread.stop()
    thread_started = False
    statusbar.set_text("  Stopping the scan ..., please wait.")
    button_ipscan_stop.set_sensitive(0)


# DEF - scan_lan
def scan_lan(obj):
    if entry_iprange.get_text() != "" and ";" not in entry_iprange.get_text():
        global tbuffer
        global thread

        thread = MyThread()

        tbuffer.set_text("\n\tScanning ..., please wait.")
        button_ipscan_stop.set_sensitive(1)
        statusbar.set_text("  Scanning the IP-range ..., please wait.")


        def start_thread():
            global thread_started
            thread_started = False
            if not thread_started:
                thread.start()
                thread_started = True

        GLib.idle_add(start_thread)
        entry_iprange.set_sensitive(0)
        button_ipscan.set_sensitive(0)


# DEF - start_portscan
def start_portscan(obj):
    global entry_host
    host = entry_host.get_text()
    x = 0
    try:
        # Attempt to resolve the address
        socket.inet_pton(socket.AF_INET, host)
        x = 1
    except socket.error:
        x = 0

    ogg = 0
    oga = 0

    if x == 1:
        title = "gLanScan - Scanning: " + host
        if os.path.exists("/usr/bin/ogg123"):
            ogg = 1
        if os.path.exists("/usr/share/sounds/Yaru/stereo/system-ready.oga"):
            oga = 1

        if ogg == 1 and oga == 1:
            status = subprocess.Popen(
                "gnome-terminal --title '" + title + "' -- bash -c 'pkexec /usr/bin/nmap -T4 -p 1-65535 -sV " + host + ";/usr/bin/ogg123 -q /usr/share/sounds/Yaru/stereo/system-ready.oga >/dev/null; sleep 5000'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()
        else:
            status = subprocess.Popen(
                "gnome-terminal --title '" + title + "' -- bash -c 'pkexec /usr/bin/nmap -T4 -p 1-65535 -sV " + host + ";sleep 5000'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            rcstat = status.wait()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here


class MyApp(Adw.Application):

    def on_key_press(self, controller, keyval, keycode, state, win):
        # Check if Ctrl+Q is pressed
        ctrl_pressed = state & Gdk.ModifierType.CONTROL_MASK
        if ctrl_pressed and keyval == Gdk.KEY_q:
            print("Ctrl+Q pressed, quitting application")
            self.quit()

        if ctrl_pressed and keyval == Gdk.KEY_m:
            print("Ctrl+Q pressed, quitting application")
            win.minimize()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        global thread
        thread = MyThread()

        win = MainWindow(application=app)
        win.set_title("gLanScan " + ver)
        win.set_default_size(800, 400)
        win.set_resizable(True)

        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_press, win)
        win.add_controller(key_controller)

        box0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        win.set_child(box0)
        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box0.append(box1)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box0.append(box2)

        label_spacer = Gtk.Label()
        box2.append(label_spacer)

        box4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box2.append(box4)

        start_label1 = Gtk.Label(label="IP-range | Host")
        start_label1.set_size_request(150, -1)
        box4.append(start_label1)

        global entry_iprange
        entry_iprange.set_max_length(40)
        entry_iprange.set_size_request(250, -1)
        #entry_iprange.connect("activate", scan_lan)
        box4.append(entry_iprange)

        global button_ipscan
        button_ipscan.set_size_request(100, -1)
        button_ipscan.connect("clicked", scan_lan)
        box4.append(button_ipscan)

        global button_ipscan_stop
        button_ipscan_stop.set_sensitive(0)
        button_ipscan_stop.set_size_request(100, -1)
        button_ipscan_stop.connect("clicked", lambda btn: stop_thread(thread))
        #box4.append(button_ipscan_stop)

        label_spacer1 = Gtk.Label()
        box2.append(label_spacer1)

        scrolled_window = Gtk.ScrolledWindow()
        global tbuffer
        textview = Gtk.TextView.new_with_buffer(tbuffer)
        scrolled_window.set_size_request(800, 400)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        textview.set_buffer(tbuffer)
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolled_window.set_child(textview)
        box2.append(scrolled_window)

        label_spacer = Gtk.Label()
        box2.append(label_spacer)

        box3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box2.append(box3)

        start_label = Gtk.Label(label="Hostname | IP")
        start_label.set_size_request(150, -1)
        box3.append(start_label)

        global entry_host
        entry_host.set_max_length(40)
        entry_host.set_size_request(250, -1)
        #entry_host.connect("activate", start_portscan)
        box3.append(entry_host)

        button_portscan = Gtk.Button(label="Scan")
        button_portscan.set_size_request(100, -1)
        button_portscan.connect("clicked", start_portscan)
        box3.append(button_portscan)

        label_spacer1 = Gtk.Label()
        box2.append(label_spacer1)

        global statusbar
        box2.append(statusbar)

        statusbar.set_halign(Gtk.Align.START)
        statusbar.set_text("  Ready.")
        tbuffer.set_text("\n\tEnter an IP-range to start a scan.")

        win.present()


# START THE APP

app = MyApp(application_id="com.sprokkel78.glanscan")
app.run(None)