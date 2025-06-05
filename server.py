import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

DATA_FILE = 'history.json'


def read_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def write_history(history):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False)


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content='text/html'):
        self.send_response(code)
        self.send_header('Content-Type', content)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    data = f.read()
                self._set_headers()
                self.wfile.write(data)
            except FileNotFoundError:
                self._set_headers(404)
        elif self.path == '/history':
            history = read_history()
            self._set_headers(content='application/json')
            self.wfile.write(json.dumps(history).encode())
        elif self.path == '/risk':
            history = read_history()
            exposure = len(history) * 1000  # 가상의 포지션 규모
            var = exposure * 0.05            # 5% VaR 예시
            self._set_headers(content='application/json')
            self.wfile.write(json.dumps({'exposure': exposure, 'VaR': var}).encode())
        else:
            self._set_headers(404)

    def do_POST(self):
        if self.path == '/trade':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
            except json.JSONDecodeError:
                self._set_headers(400)
                return
            history = read_history()
            history.append(data)
            write_history(history)
            self._set_headers(content='application/json')
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self._set_headers(404)


def run(port=8000):
    server = HTTPServer(('', port), Handler)
    print(f'Server running on http://localhost:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run()
