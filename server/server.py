from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import hashlib
import threading
import socket

host = "localhost"
PORT = 8000
TOKENS = {}

def gerar_token(usuario):
    return hashlib.sha256(usuario.encode()).hexdigest()

class API(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/login":
            self.send_response(404)
            self.end_headers()
            return

        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0:
            self.send_response(400)
            self.end_headers()
            return

        corpo = self.rfile.read(tamanho)
        dados = json.loads(corpo.decode())

        usuario = dados.get("user")
        senha = dados.get("password")

        with open("users.json") as f:
            users = json.load(f)

        if usuario in users and users[usuario]["password"] == senha:
            token = gerar_token(usuario)
            TOKENS[token] = users[usuario]["role"]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"token": token}).encode())
        else:
            self.send_response(401)
            self.end_headers()

    def do_GET(self):
        if self.path != "/soma":
            self.send_response(404)
            self.end_headers()
            return

        auth = self.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            self.send_response(403)
            self.end_headers()
            return

        token = auth.replace("Bearer ", "")
        if token not in TOKENS:
            self.send_response(403)
            self.end_headers()
            return

        resultado = 10 + 20
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"resultado": resultado}).encode())

def socket_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 9000))
    s.listen(1)
    print("Socket TCP rodando em localhost:9000")

    while True:
        cliente, _ = s.accept()
        msg = cliente.recv(1024).decode()
        cliente.send(f"Recebido: {msg}".encode())
        cliente.close()

# 🔥 socket em thread
threading.Thread(target=socket_server, daemon=True).start()

# 🔥 API
server = HTTPServer((host, PORT), API)
print("API REST rodando em http://localhost:8000")
server.serve_forever()
