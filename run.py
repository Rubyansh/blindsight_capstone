#!/usr/bin/env python3
"""
Main entry point for Blind Vision Assistant
Run this file to start the web application
"""

import os
import sys
from src.web_app import app

if __name__ == '__main__':
    print("Starting Blind Vision Assistant...")
    print("Web interface available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)