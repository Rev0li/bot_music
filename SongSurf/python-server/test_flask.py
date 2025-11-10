#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("🚀 Test Flask - Démarrage...")
    print("📁 Templates:", app.template_folder)
    print("📁 Static:", app.static_folder)
    print("🌐 Serveur: http://localhost:5000")
    print("-" * 50)
    
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)
