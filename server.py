import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def server_rec():

    while True:
        server = socket.socket()
        server.bind((socket.gethostname(), 9971))
        server.listen()
        client, addr = server.accept()
        print("Client connected:", addr)

        file_name, file_size = client.recv(1024).decode().split("<SEP>")
        print("Received file name:", file_name)
        print("Received file size:", file_size)
        file_path = "D:/fileX/{}".format(file_name)
        file = open(file_path, "wb")
        file_bytes = b""
        done = False

        requests.post('http://localhost:3001/transfer_rate', json={
            "ip": addr[0],
            "status_code": False,
            "host": "jayLinux",
            "file_name": file_name,
            "file_size": int(file_size) / 1000000,
            "file_path": file_path,
        })

        while not done:
            data = client.recv(int(file_size))
            if file_bytes[-5:] == b"<END>":
                done = True
            file_bytes += data

        requests.post('http://localhost:3001/transfer_rate', json={
            "ip": addr[0],
            "status_code": True,
            "host": "jayLinux",
            "file_name": file_name,
            "file_size": int(file_size) / 1000000,
            "file_path": file_path,
        })
        file.write(file_bytes)
        file.close()
        print("File received:", file_path)
        server.close()
        client.close()

server_rec()