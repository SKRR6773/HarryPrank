import socket
import ipaddress
from check_ips import iface_link


my_ip = iface_link.get("addr")


serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


serv.sendto(my_ip.encode(), ("<broadcast>", 6773))

serv.close()