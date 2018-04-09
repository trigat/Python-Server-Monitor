# Run PowerShell scripts on timer
import multiprocessing
import time
import sys
import os
import subprocess

def run_services(queue):
    while True:
        print ("Running PowerShell Service Check")
        try:
            queue = subprocess.call(["powershell.exe", "-command", "./svcMonitor.ps1"])
        except FileNotFoundError as error:
            print("\nError: PowerShell not found or not running properly.")
        time.sleep(40)

if __name__ == '__main__':

    # for testing
    queue = multiprocessing.Queue()
    run_services(queue)
