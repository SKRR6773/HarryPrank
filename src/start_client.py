from utils.check_platform import is_linux
from client.HandShake import HandShake
from threading import Thread
from client.Client import Client
from client.logger import info
import client.shared as shared
from utils.check_ips import gethostname
from utils.env import SERVER_PORT, EX_SERVER_PORT
import time
import sys
import os


__DIR__ = os.path.dirname(__file__)



if __name__ == "__main__":
    pid = str(os.getpid())

    info("OS is " + "linux" if is_linux else "windows")
    


    args = sys.argv[1:]

    if len(args) > 0:
        # print(args)

        if args[0] == "check_dir":
            print(os.path.dirname(__file__))
            input("Enter to exit")
            sys.exit(0)

            
    info("Listening Server")
    info(f"Process ID: {pid}")


    with open(os.path.join(__DIR__, "proc.pid"), 'w', encoding="utf-8")as fw:
        fw.write(pid)



    while shared.is_running:
        try:
            shared.hand_shake = HandShake()
            task = Thread(target=shared.hand_shake.listening, args=())
            task.start()



            while shared.is_running:
                try:
                    

                    if shared.hand_shake.serverIP:
                        shared.hand_shake.close()
                        shared.server_ip = shared.hand_shake.serverIP
                        info(f"Server Connected::{shared.server_ip}")

                        shared.client = Client(shared.server_ip, SERVER_PORT)
                        shared.client.run_forest()

                        break


                    else:
                        hostname = gethostname()


                        if hostname:
                            shared.hand_shake.close()
                            shared.server_ip = hostname
                            info(f"External Server Connected::{shared.server_ip}")

                            shared.client = Client(shared.server_ip, EX_SERVER_PORT)
                            shared.client.run_forest()

                            break



                    time.sleep(3)


                except KeyboardInterrupt as ex:
                    print(ex)
                    shared.is_running = False
                    break


                except Exception as ex:
                    raise ex
                


        except KeyboardInterrupt as ex:
            print(ex)
            shared.is_running = False
            break


        except Exception as ex:
            print(ex)
            time.sleep(5)

