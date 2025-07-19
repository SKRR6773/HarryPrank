# start_server.py
from server.HelloClient import HelloClient
from threading import Thread
from server.Server import Server
from server.logger import info
import server.shared as shared




if __name__ == "__main__":
    info("Listening bot")
    info("Processes starting")

    info("Server TCP Starting")
    shared.server = Server()   # Enemy Of Server

    task = Thread(target=shared.server.listening, args=())
    task.start()
    shared.main_tasks.append(task)
    info("Server TCP Started")


    info("HelloClient Server Starting")
    shared.hello_client = HelloClient()

    task = Thread(target=shared.hello_client.broadcast, args=())
    task.start()
    shared.main_tasks.append(task)
    info("HelloClient Started")



    for task in shared.main_tasks:
        task.join()



    info("All Service Closed")
    