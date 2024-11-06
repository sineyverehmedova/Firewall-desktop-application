import gi
import subprocess
import nmap
import socket
import time

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import Notify

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="IP && Paket")
        self.set_border_width(10)
        self.set_size_request(200,100)
        Notify.init("IP bloklama və paket göndərmə proqramı")

        

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)

        self.ip = Gtk.Entry()
        self.ip.set_text("IP")
        vbox.pack_start(self.ip, True, True, 0)


        button1 = Gtk.Button(label="IP-ni blokla")

        button1.connect("clicked", self.on_button_clicked_1)
        vbox.pack_start(button1, True, True, 0)

        button2 = Gtk.Button(label="IP-ni blokdan çıxart")

        button2.connect("clicked", self.on_button_clicked_2)
        vbox.pack_start(button2, True, True, 0)


        button3 = Gtk.Button(label="IP-ə TCP paket göndər")

        button3.connect("clicked", self.on_button_clicked_3)
        vbox.pack_start(button3, True, True, 0)


        button4 = Gtk.Button(label="IP-ə UDP paket göndər")

        button4.connect("clicked", self.on_button_clicked_4)
        vbox.pack_start(button4, True, True, 0)        


        button5 = Gtk.Button(label="IP-ə ICMP paketi göndər")

        button5.connect("clicked", self.on_button_clicked_5)
        vbox.pack_start(button5, True, True, 0)


        self.port = Gtk.Entry()
        self.port.set_text("Port")
        vbox.pack_start(self.port, True, True, 0)


        self.message = Gtk.Entry()
        self.message.set_text("Mesaj")
        vbox.pack_start(self.message, True, True, 0)


        button6 = Gtk.Button(label="IP-ə xüsusi port üzərindən mesaj göndər")

        button6.connect("clicked", self.on_button_clicked_6)
        vbox.pack_start(button6, True, True, 0)


    def on_button_clicked_1(self,widget):
            
        scanner = nmap.PortScanner()
        host = socket.gethostbyname(self.ip.get_text())
        scanner.scan(host,'1','-v')

        if scanner[host].state() == "up":
            subprocess.run(["iptables","-I","INPUT","-s",self.ip.get_text(),"-j","DROP"])
            subprocess.run(["iptables","-I","OUTPUT","-d",self.ip.get_text(),"-j","DROP"])

            n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "IP uğurla bloklandı !")
            n.show()
            
        elif scanner[host].state() == "down":
            n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "IP işlək deyil !")
            n.show()
        
    
    def on_button_clicked_2(self,widget):

        subprocess.run(["iptables","-D","INPUT","-s",self.ip.get_text()+'/32',"-j","DROP"])
        subprocess.run(["iptables","-D","OUTPUT","-d",self.ip.get_text()+'/32',"-j","DROP"])

        n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "IP uğurla blokdan çıxarıldı !")
        n.show()
    
    def on_button_clicked_3(self,widget):

        n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "TCP paketi uğurla göndərildi !")
        n.show()

    def on_button_clicked_4(self,widget):

        n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "UDP paketi uğurla göndərildi !")
        n.show()

    def on_button_clicked_5(self,widget):

        n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "ICMP paketi uğurla göndərildi !")
        n.show()

    def on_button_clicked_6(self,widget):

        scanner = nmap.PortScanner()
        host = socket.gethostbyname(self.ip.get_text())
        scanner.scan(host,'1','-v')

        if scanner[host].state() == "up":

            a =  Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "Diqqət ! Əgər qarşı tərəf həmin portu dinləmirsə, mesaj getməyəcək.")
            a.show()
            message = "\n" + str(self.message.get_text()) + "\n\n"
            connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connection.connect((self.ip.get_text(),int(self.port.get_text())))
            bytes = str(message).encode(encoding="latin1")
            connection.send(bytes)
                
            n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "Mesaj uğurla göndərildi !")
            n.show()

        elif scanner[host].state() == "down":
            n = Notify.Notification.new("IP bloklama və paket göndərmə proqramı", "IP işlək deyil !")
            n.show()





win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()