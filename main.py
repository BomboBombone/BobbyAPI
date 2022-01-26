import cgi
import os

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
        statement = 'Hi'
        chat_id = 0
        server_id = 0
        default = 0
        prev_statement = 'Hello'
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
                default = int(payload["default"])
            except:
                pass
            try:

                chat_id = int(payload["chat_id"])
                statement = payload["text"]
                prev_statement = payload["prev_text"]
            except Exception as ex:
                try:
                    server_id = int(payload["server_id"])
                except:
                    pass

        if request_type.startswith('/chat'):
            if chat_id:
                statement = urllib.parse.unquote(statement)
                prev_statement = urllib.parse.unquote(prev_statement)
                bot = chatbot.get_bot_from_ID(chat_id)
                if bot is None:
                    self.send_error(404)
                    return
                if prev_statement != "Hello":
                    try:
                        if int(os.path.getsize(str(chat_id) + '.db')) < 3000000:
                            if default:

                                self.send_response(205)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                self.wfile.write(bytes('', 'utf-8'))
                                chatbot.trainer.train([prev_statement, statement])
                                print('Trained for default database')
                            else:
                                self.send_response(204)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                self.wfile.write(bytes('', 'utf-8'))
                                bot.train(statement, prev_statement)
                    except:
                        self.send_error(500)
                else:
                    res = bot.get_response(statement)
                    if res is None:
                        self.send_error(501, 'Invalid text')
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(bytes(res.text, 'utf-8'))
            else:
                if server_id:
                    bot = chatbot.get_bot_from_ID(server_id)
                    if bot is None:
                        bot = chatbot.chatbot(server_id)
                    response = '{"chat_id":' + str(bot.ID) + '}'
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(response, 'utf-8'))


def main():
    import pathlib

    cur_path = pathlib.Path(__file__).parent.absolute()

    for file in os.listdir(cur_path):
        if file.endswith('.db') and file != 'database.db':
            chatbot.chatbot(int(file.split('.')[0]))
            print('Loaded chats for server: ' + file.split('.')[0])
    #    if file.endswith('.db-shm') and file != 'database.db-shm':
    #        os.remove(file)
    #        print('Deleted unused database: ' + file)
    #    if file.endswith('.db-wal') and file != 'database.db-wal':
    #        os.remove(file)
    #        print('Deleted unused database: ' + file)
    Handler = ChatBotAIServer

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Http Server Serving at port", PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
