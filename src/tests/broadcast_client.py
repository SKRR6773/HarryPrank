import socket




serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
serv.bind(('', 6773))
serv.settimeout(3)



while True:
    try:
        data, addr = serv.recvfrom(1024)

        print(addr)
        print(data)



    except KeyboardInterrupt:
        break

    except TimeoutError:
        print("timeout")

        continue


    except Exception as ex:
        print(ex)



serv.close()

