from http.server import BaseHTTPRequestHandler, HTTPServer
import json

alunos = [
    {"id": 1, "nome": "ana", "idade": 15},
    {"id": 2, "nome": "carlito", "idade": 16}
]

class Api(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/alunos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            resposta = json.dumps(alunos)
            self.wfile.write(resposta.encode("utf-8"))

        elif self.path.startswith("/api/alunos/"):
            try:
                id_aluno = int(self.path.split("/")[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"ID invalido")
                return

            aluno_encontrado = None

            for aluno in alunos:
                if aluno["id"] == id_aluno:
                    aluno_encontrado = aluno
                    break

            if aluno_encontrado:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                resposta = json.dumps(aluno_encontrado)
                self.wfile.write(resposta.encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps(
                    {"erro": "aluno nao encontrado"}
                ).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps(
                {"erro": "rota nao encontrada"}
            ).encode("utf-8"))


def main():
            servidor = HTTPServer(("localhost", 8000), Api)
            print("Servidor rodando em http://localhost:8000")
            servidor.serve_forever()
        
if __name__ == "__main__":
    main()
