#!/usr/bin/env python3
"""
Simple HTTP server for local development of the Library Management System frontend.

This script starts a local HTTP server to serve the frontend files from the current directory.
This allows you to test the frontend application locally before deploying to GitHub Pages.

Usage:
    python start_server.py

The server will start on http://localhost:8080 by default.
"""

import http.server
import socketserver
import os
import sys
from functools import partial

class CORSEnabledHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers enabled"""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def main():
    port = 8080
    handler = partial(CORSEnabledHTTPRequestHandler, directory=os.getcwd())
    
    print(f"Starting local server on http://localhost:{port}")
    print(f"Serving files from: {os.getcwd()}")
    print("Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        return 0

if __name__ == "__main__":
    sys.exit(main())