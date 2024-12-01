import multiprocessing
import socket
import botStarter as bs
import time


class ping_thing:
    def __init__(self):
        address = "1.1.1.1"
        port = "80"
        processes = []

        while True:
            self.internet_alive = self.ping(address, port)
            print(f"Is Internet up? : {internet_alive}")

            if self.internet_alive == True:
                print("starting bot")
                discord_process = multiprocessing.Process(target=bs.Start_Bot)
                ping_process = multiprocessing.Process(target=self.ping_server)

                discord_process.start()
                ping_process.start()
                processes.append(discord_process)
                processes.append(ping_process)

            elif self.internet_alive == False:
                for process in processes:
                    process.terminate()
                    process.join()
                    print("All child processes terminated")

            time.sleep(10)



    def ping_server(self, address: str, port: int):
        """ping server"""
        try:
            timeout = 3
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, port))
        except OSError as error:
            return False
        else:
            s.close()
            return True
    
    


if __name__ == "__main__":

    processes = []

    internet_alive = ping_server("1.1.1.1", 80)
    print(f"Is Internet up? : {internet_alive}")
    time.sleep(2)

    if internet_alive == True:
        print("starting bot")
        discord_process = multiprocessing.Process(target=bs.Start_Bot)
        ping_process = multiprocessing.Process(target=)
        discord_process.start()
        processes.append(discord_process)
        


    time.sleep(5)  # Let the child processes run for 5 seconds
    print("Terminating all child processes")
    for process in processes:
        process.terminate()
        process.join()