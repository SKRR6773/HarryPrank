import netifaces



iface_link = None

for iface in netifaces.interfaces():
    if iface_link:
        break


    if netifaces.AF_INET in netifaces.ifaddresses(iface):
        for link in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
            if iface_link:
                break


            if link.get("addr") == "127.0.0.1":
                continue

            iface_link = link



            break


IPV4 = iface_link.get("addr")
IPBROADCAST = iface_link.get("broadcast")