from http.server import BaseHTTPRequestHandler, HTTPServer
import json

alunos = [
    {"id": 1, "nome": "ana", "idade": 15},
    {"id": 2, "nome": "carlito", "idade": 16},
    {"id": 3, "nome": "ana", "idade": 15}
]

# gera id automaticamente
def proximo_id():
    if not alunos:
        return 1
    return max(aluno["id"] for aluno in alunos) + 1


class Minhaapi(BaseHTTPRequestHandler):

    # ================= GET =================
    def do_GET(self):

        if self.path == "/alunos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(alunos).encode("utf-8"))

        elif self.path == "/api/alunos/tamanho":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(
                {"total": len(alunos)}
            ).encode("utf-8"))

        elif self.path.startswith("/api/alunos/"):
            try:
                id_aluno = int(self.path.split("/")[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"ID invalido")
                return

            for aluno in alunos:
                if aluno["id"] == id_aluno:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(aluno).encode("utf-8"))
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps(
                {"erro": "aluno nao encontrado"}
            ).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    # ================= POST =================
    def do_POST(self):

        if self.path == "/alunos":
            tamanho = int(self.headers["Content-Length"])
            corpo = self.rfile.read(tamanho)
            dados = json.loads(corpo)

            novo_aluno = {
                "id": proximo_id(),
                "nome": dados.get("nome"),
                "idade": dados.get("idade")
            }

            alunos.append(novo_aluno)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(novo_aluno).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    # ================= PUT =================
    def do_PUT(self):

        if self.path.startswith("/api/alunos/"):
            try:
                id_aluno = int(self.path.split("/")[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return

            tamanho = int(self.headers["Content-Length"])
            corpo = self.rfile.read(tamanho)
            dados = json.loads(corpo)

            for aluno in alunos:
                if aluno["id"] == id_aluno:
                    aluno["nome"] = dados.get("nome", aluno["nome"])
                    aluno["idade"] = dados.get("idade", aluno["idade"])

                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(aluno).encode("utf-8"))
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Aluno nao encontrado")

        else:
            self.send_response(404)
            self.end_headers()

    # ================= DELETE =================
    def do_DELETE(self):

        if self.path.startswith("/api/alunos/"):
            try:
                id_aluno = int(self.path.split("/")[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return

            for i, aluno in enumerate(alunos):
                if aluno["id"] == id_aluno:
                    alunos.pop(i)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Aluno removido")
                    return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Aluno nao encontrado")

        else:
            self.send_response(404)
            self.end_headers()


def main():
    servidor = HTTPServer(("localhost", 8000), Minhaapi)
    print("Servidor rodando em http://localhost:8000")
    servidor.serve_forever()


if __name__ == "__main__":
    main()
