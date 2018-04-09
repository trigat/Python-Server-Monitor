# Ping servers and log
import multiprocessing
import subprocess
import platform  # checks the OS
import shutil
import time
import csv
import sys
import os

def run_ping(queue):

    while True:
        print("Pinging")
        time.sleep(3)  # CHANGE TIME HERE
        try:
            otherDir = 'log'  # specify log direcotry
            origDir = os.getcwd()
            os.chdir(os.path.join(os.path.abspath(sys.path[0]), otherDir)) # switch to other dir
        except OSError:
            print("Error: 'log' directory does not exist.")
            break
        try:
            open('./srvlog.csv', 'w').close()  # clears the log before scan
            #print("\nOS is " + platform.system().lower() + ":\n")
            with open(os.devnull, "wb") as intothevoid:
                with open("../list/servers.txt", "r") as hostname:
                    for x in hostname:
        
                        if platform.system().lower() == 'windows':
                            osFlag = '-n' 
                        else:
                            osFlag = '-c'  # Linux/etc

                        output = subprocess.Popen(["ping", osFlag, "1", "-w", "1900", x.strip()],
                                            stdout=intothevoid, stderr=intothevoid).wait()
        
                        with open("./srvlog.csv", "a", newline='') as document:  # newline prevents blank lines
        
                            writer = csv.writer(document)
                            mid    = ["is"]
                            endNo  = ["Offline"]
                            endYes = ["Online"]
                            if output:
                                    offline = [x.replace('\n','')]  # formats properly from ping output
                                    print(offline)  # for testing
                                    writer.writerows([offline + mid + endNo])
                            else:
                                    online = [x.replace('\n','')]
                                    print(online)
                                    writer.writerows([online + mid + endYes])
                            document.close()
        except IOError as e:
            print (e)
            time.sleep(30)
        try:
            shutil.copy('./srvlog.csv', './srvlogLive.csv')
        except Error as err:
            errors.extend(err.args[0])
        os.chdir(origDir) # switch back

if __name__ == '__main__':

    queue = multiprocessing.Queue()
    run_ping(queue)
