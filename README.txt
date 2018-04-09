Python Server Monitor - Installation
Copyright (C) 2018, Josh M

Python Server Monitor uses both Python and PowerShell for monitoring servers and services running on a network.  
This program was written in Python 3 on Windows 7.  It can probably run on Linux easily but you would have
to check services with something other than PowerShell.

It was written for testing purposes and may not be secure.

Please feel free to edit and improve this!


1.  Place the PyServerMonitor folder with all contents on your computer.  For example:
    C:\Users\YourName\Desktop\pyServerMonitor

2.  Install the Matplotlib module for Python.  Run this command at the command prompt:
    pip install matplotlib

    Make sure your Execution Policy is set properly to allow you to run PowerShell scripts.

3.  Open the main.py file in the main directory with a text editor.  Fill in your computer's IP address in the IP variable.
    You can also change the port if you like.  Save the file.

4.  Go to the 'list' directory and open the servers.txt and services.txt files.
    Place the list of servers you want to monitor in the servers.txt.  Place your service names in the services.txt.
    When you do this, place one name on each line.

5.  Run main.py

    You should be up and running.  Open your browser and enter your IP:port number into the URL bar.  Example:
    http://10.1.177.198:8080

**Note**

This program auto refreshes your browser so that you can view up-to-date information.
Sometimes the browser has this option disabled.
You can turn off the block auto refresh feature in Firefox.

Go to URL bar and type about:config.  
Go to:
accessibility.blockautorefresh
Set to False.
