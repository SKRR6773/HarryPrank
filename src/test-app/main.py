from threading import Thread
from typing import List
import time
import os


__DIR__ = os.path.dirname(__file__)



class Updater:
    def __init__(self):
        print("Updater Start")


class Main:
    def __init__(self):
        print("Main App Start")

        file_path = os.path.join(__DIR__, "result.txt")

        if os.path.exists(file_path):
            os.remove(file_path)


        
        for i in range(1000):
            # print(i)
            with open(file_path, 'a', encoding='utf-8')as fw:
                fw.write(str(i) + "\n")
                time.sleep(1)





tasks: List[Thread] = []



if __name__ == "__main__":
    for proc in [
        Updater,
        Main
    ]:
        task = Thread(target=proc, args=())
        task.start()
        tasks.append(task)



    
    for task in tasks:
        task.join()


    print("END")