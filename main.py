# Python Server Monitor - Monitor servers and services in a network.
# Copyright (C) 2018, Josh M <trigat@protonmail.com>                     


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Make sure you input your IP address below.

import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from os import curdir, sep
from itertools import islice
from os import path

import time
import sys
import os

import chart
import pshell
import ping

IP = '10.1.116.172'  # CHANGE IP AND PORT
PORT = 8080

origDir = os.getcwd()

class myServer(BaseHTTPRequestHandler):

#**************************** BEGIN OF HTML CONTENT ****************************

    def refresh_page(self):
        self.wfile.write(bytes("<meta http-equiv='refresh' content='30' />", "utf8"))

    def title(self):
        self.wfile.write(bytes("<div id='title'><img src='../static/images/title.png'></div>", "utf8"))

    def containerDIV(self):
        self.wfile.write(bytes("<div id='container'>", "utf8"))

    def subTitle(self): # EDIT THIS FOR THE AVERAGE TIME IT TAKES BASED ON YOUR SERVER LIST
        self.wfile.write(bytes("<font color='#729fcf' face='verdana, sans-serif, palatino' size='.5em'><p>Server and service scan refreshes every " \
            "40-60 seconds.</font>", "utf8"))

    def serviceStopped(self):

        with open(origDir + "/log/svclogLive.csv", "r") as f:
            strings = ("Stopped", "Manual", "Disabled")  # Search for these service status terms in the log
            for line in f:
                if any(s in line for s in strings):                                                                                 # line.replace formats data obtained from PowerShell CSV
                    self.wfile.write(bytes("<td id='wrapword'><font color='#8ae234' face='verdana, sans-serif, palatino' size='.11em'><p>" + line.replace(',', '<br>').replace('"', '').replace('.Service', '') + "</font>" \
                        "<img src='../static/images/cog.png' alt='Server Red' style='width:25px;height:25px;'><td>", "utf8"))              # This is customized based on Service names I am monitoring.

    def serverOffline(self):
        with open(origDir + "/log/srvlogLive.csv", "r") as f:
            for line in f:
                if "Offline" in line:
                    self.wfile.write(bytes("<td><font color='#8ae234' face='verdana, sans-serif, palatino' size='.11em'><p>" + line.replace(',', ' ').replace('"', '').replace('is', '') + "</font>" \
                        "<img src='../static/images/redserver.png' alt='Server Red' style='width:50px;height:17px;'></td>", "utf8"))

    def serverOnline(self):
        with open(origDir + "/log/srvlogLive.csv", "r") as f:
            for line in f:
                if "Online" in line:
                    self.wfile.write(bytes("<td><font color='#8ae234' face='verdana, sans-serif, palatino' size='.11em'><p>" + line.replace(',', ' ').replace('"', '').replace('is', '') + "</font>" \
                        "<img src='../static/images/greenserver.png' alt='Server Red' style='width:50px;height:17px;'></td>", "utf8"))

    def stopSection(self):  # tables are used for these sections
        self.wfile.write(bytes("<br><br><br>", "utf8"))
        self.wfile.write(bytes("<div id='divider'>Service Monitor</div>", "utf8"))
        self.wfile.write(bytes("<br>", "utf8"))
        self.wfile.write(bytes("<table>", "utf8"))
        self.wfile.write(bytes("<tr>", "utf8"))
        self.serviceStopped()
        self.wfile.write(bytes("</tr>", "utf8"))
        self.wfile.write(bytes("</table>", "utf8"))

    def offlineSection(self):
        self.wfile.write(bytes("<br><br><br>", "utf8"))
        self.wfile.write(bytes("<div id='divider'>Servers Offline</div>", "utf8"))
        self.wfile.write(bytes("<br>", "utf8"))
        self.wfile.write(bytes("<table>", "utf8"))
        self.wfile.write(bytes("<tr>", "utf8"))
        self.serverOffline()
        self.wfile.write(bytes("</tr>", "utf8"))
        self.wfile.write(bytes("</table>", "utf8"))

    def onlineSection(self):
        self.wfile.write(bytes("<br><br><br>", "utf8"))
        self.wfile.write(bytes("<div id='divider'>Servers Online</div>", "utf8"))
        self.wfile.write(bytes("<br>", "utf8"))
        self.wfile.write(bytes("<table>", "utf8"))
        self.wfile.write(bytes("<tr>", "utf8"))
        self.serverOnline()  
        self.wfile.write(bytes("</tr>", "utf8"))
        self.wfile.write(bytes("</table>", "utf8"))

    def endDIV(self):
        self.wfile.write(bytes("</div>", "utf8"))

    def otherImages(self):  # Dont write this yet because we may have to edit the path that the button links to
        return["<div id='chart'><img src='../static/images/main_chart.png'></div><div id='menu_button'><a href='/narrow'><img src='../static/images/menu_button.png'></a></div>"]

#**************************** END OF HTML CONTENT ****************************

    def contentList(self, skip_names=''):  # All content functions in list 
        methods = [self.refresh_page, self.title, self.containerDIV, self.subTitle, self.stopSection, self.offlineSection, self.onlineSection, self.endDIV, self.otherImages]
        for m in methods:
            if m.__name__ not in skip_names:
                m()

    def reply(self):
        sendReply = False
        if self.path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if self.path.endswith(".png"):
            mimetype='image/png'
            sendReply = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True
        if sendReply == True:
            #Open the static file requested and send it
            f = open(curdir + sep + self.path, 'rb')
            # Send response status code
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

    def narrow(self):  # IP:PORT/narrow
        try:
            self.reply()
            self.contentList({'onlineSection'})   # removed onlineSection
            for words in self.otherImages():
                words = words.replace("/narrow", "/")  # change path for button hyperlink
                self.wfile.write(bytes(words, "utf8"))
            return			

        except IOError:
            return
            # self.send_error(404,'File Not Found: %s' % self.path)

    # GET
    def do_GET(self):  # index page of site
        if self.path=="/":
            self.path="/static/views/index.html"
        if self.path=="/narrow":
            self.path="/static/views/narrow.html"
            self.narrow()
            return
        if self.path == "/static/images/favico.ico":
            return
        try:
            self.reply()
            self.contentList()
            for words in self.otherImages():
                self.wfile.write(bytes(words, "utf8"))
            return

        except IOError:
            return
            # self.send_error(404,'File Not Found: %s' % self.path)

class QueuingHTTPServer(ThreadingMixIn, HTTPServer):  #  Add ThreadingMixIn so that server is threaded.
    #  This prevents Internet Explorer requests from hanging up the server.

    # def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, queue=False):
    def __init__(self, server_address, RequestHandlerClass, queue, bind_and_activate=True):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.queue = queue

def run_server(queue):
    try:
        print('Starting server...')     
        server_address = (IP, PORT)
        httpd = QueuingHTTPServer(server_address, myServer, queue)
        httpd.timeout = 20
        print ('Started HTTP server on port ' , IP, PORT)
        while True:
            httpd.handle_request()
        #httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down the web server.')
        httpd.socket.close() 
    except IOError as e:
        print (e)
        print ("Note: Check your IP address.")


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_server, args=(queue,))

    # Call from modules
    p2 = multiprocessing.Process(target=ping.run_ping, args=(queue,))
    p3 = multiprocessing.Process(target=pshell.run_services, args=(queue,))
    p4 = multiprocessing.Process(target=chart.main_chart, args=(queue,))
    p.start()
    p2.start()
    p3.start()
    p4.start()


# *This has not been tested yet.*
# Example of how to run HTTPS server:
#
#import BaseHTTPServer, SimpleHTTPServer
#import ssl
#
#httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
#httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
#httpd.serve_forever()
