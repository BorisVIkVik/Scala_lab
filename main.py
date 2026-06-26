import os
from src.model import clasterisation
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/api/endpoint', methods=['POST'])
def handle_post():
    data = request.json
    centers = clasterisation()
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(port=5000)
