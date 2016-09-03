
from tornado import websocket, web, ioloop
import json
clients = {}

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clients:
            clients[self] = 0
        data = {"sum": sum(clients.itervalues())}
        data = json.dumps(data)
        self.write_message(data)


    def on_close(self):
        clients.pop(self, None)

    def on_message(self, message):
        try:
            n = int(message)
        except (TypeError, ValueError):
            data = {"error": 'Sending not a number'}
            data = json.dumps(data)
            self.write_message(data)
            return

        if not ( 0<n<=10):
            data = {"error": 'Number must be between 1 and 10'}
            data = json.dumps(data)
            self.write_message(data)
            return

        clients[self] = n

        self.send_sum()




    def send_sum(self):
        data = {"sum": sum(clients.itervalues())}
        data = json.dumps(data)
        for client in clients.iterkeys():
            client.write_message(data)




app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()