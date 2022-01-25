import cgi

from AI import chatbot
import http.server  # Our http server handler for http requests
import socketserver  # Establish the TCP Socket connections
import urllib.parse
import json

PORT = 9000

def get_content_length(headers: list):
    for header in headers:
        if "content-length" in header.strip().lower():
            length = header.split(':')[1].strip()
            return length
    return None

def get_auth_token(headers: list):
    for header in headers:
        if "Authorization" in header.strip():
            if header.split(':')[1].strip().startswith("Bearer"):
                token = header.split(':')[1].strip().split(' ')[1].strip()
                return token
    return None

class ChatBotAIServer(http.server.SimpleHTTPRequestHandler):
    def address_string(self):
        host, port = self.client_address[:2]
        # return socket.getfqdn(host)
        return host

    def do_POST(self):
        request_type = self.path
        if request_type.startswith('/api'):
            request_type = request_type.replace('/api', '')
        queries = []
        name = 'Bobby'
        chat_id = 0
        statement = 'Hi'
        if '?' in request_type:
            queries = request_type.split('?')[1].split('&')
            request_type = request_type.split('?')[0]
        for query in queries:
            if 'name' in query:
                name = query.split('=')[1].strip()

        ctype, pdict = cgi.parse_header(self.headers.get_content_type())
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400, 'Unsupported')
            self.end_headers()
            return
        if name == 'Bobby':
            try:
                length = get_content_length(self.headers.as_string().split('\n'))
                payload = json.loads(self.rfile.read(int(length)))
                chat_id = payload["chat_id"]
                statement = payload["text"]
            except Exception as ex:
                pass

        if request_type.startswith('/chat'):
            statement = urllib.parse.unquote(statement)
            res = chatbot.bot.get_response(statement)
            if res is None:
                self.send_error(501, 'Invalid text')
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(res.text, 'utf-8'))

def main():
    Handler = ChatBotAIServer

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Http Server Serving at port", PORT)
        httpd.serve_forever()

if __name__ == '__main__':
    main()
