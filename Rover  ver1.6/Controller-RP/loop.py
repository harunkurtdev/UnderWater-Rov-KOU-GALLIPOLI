from flask import Flask,render_template, Response
import json
import base64
import io
import asyncio
import websockets
import cv2
import numpy as np
from webSocketsOpencvServer import RovCamSocketsTransfer
"""
loop dosyası içerisinde programımızın akışı sağlanacaktır..
resimler flask üzerinden webBrowser da gösterebileceğimiz şekilde olabilmesini sağlamaktır.
aynı zamanda kurulan server da request atarak görevlerimizin tanımlamalarını yapabilir hale getirmek amacımız.

"""
rovCamSocketsTransfer=None

app=Flask(__name__)

@app.route("/")
def main():

    return "Giriş"



if __name__ == '__main__':

    app.run(host="localhost",port=5002,debug=True,use_reloader=True,threaded=True)