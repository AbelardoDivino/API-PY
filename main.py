from http.server import BaseHTTPRequestHandler, HTTPServer
#basehttp fornece os metodos para lidar com GET,POST...

import json

alunos = [
    {"id": 1, "nome":"ana", "idade": 15},
    {"id": 2, "nome":"carlito", "idade": 16}
]

class Minhaapi(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/alunos":
            self.send_response(200)
            #enviar status para cliente
            self.send_header("content-Type", "application/json")
            # send.header = enviar o cabeçalho  http type vai informar o tipo de conteudo 
            self.end_headers() #finalizar o cabeçalho para enviar
            resposta = json.dumps(alunos) # converte a lista em python em string
            self.wfile.write(resposta.encode("utf-8"))
