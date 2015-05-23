import zmq
import threading


class Server(object):

    def __init__(self, name, state, log, messageBoard, neighbors):
        self._name = name
        self._state = state
        self._log = log
        self._messageBoard = messageBoard
        self._neighbors = neighbors
        self._total_nodes = 0

        self._commitIndex = 0
        self._currentTerm = 0

        self._lastApplied = 0

        self._lastLogIndex = 0
        self._lastLogTerm = None

        self._state.set_server(self)
        self._messageBoard.set_owner(self)

    def send_message(self, message):
        for n in self._neighbors:
            message._receiver = n._name
            n.post_message(message)

    def send_message_response(self, message):
        n = [n for n in self._neighbors if n._name == message.receiver]
        if(len(n) > 0):
            n[0].post_message(message)

    def post_message(self, message):
        self._messageBoard.post_message(message)

    def on_message(self, message):
        state, response = self._state.on_message(message)

        self._state = state


class ZeroMQServer(Server):
    def __init__(self, name, state, log, messageBoard, neighbors, port=6666):
        super(ZeroMQServer, self).__init__(name, state, log, messageBoard, neighbors)
        self._port = 6666

        class SubscribeThread(threading.Thread):
            def run(thread):
                context = zmq.Context()
                socket = context.socket(zmq.SUB)
                for n in neighbors:
                    socket.connect("tcp://%s:%d" % (n._name, n._port))

                while True:
                    message = socket.recv()
                    self.on_message(message)

        class PublishThread(threading.Thread):
            def run(thread):
                context = zmq.Context()
                socket = context.socket(zmq.PUB)
                socket.bind("tcp://*:%d" % self.port)

                while True:
                    message = self._messageBoard.get_message()
                    socket.send(message)

        self.subscribeThread = SubscribeThread()
        self.publishThread = PublishThread()

        self.subscribeThread.daemon = True
        self.subscribeThread.start()
        self.publishThread.daemon = True
        self.publishThread.start()
