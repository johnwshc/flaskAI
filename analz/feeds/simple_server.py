# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 12:48:00 2018

@author: johnc
"""

import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()