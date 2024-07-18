#!/usr/bin/env python3
'''
return a JSON payload of the form:

{"message": "Bienvenue"}
'''
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def payload():
    '''returns a JSON payload of form'''
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
