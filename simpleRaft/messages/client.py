#!/usr/bin/python
'''
Slightly different class type needed for Client<->Raft communication
This is not pub/sub due to the un-announced nature of clients
Each server shall run a req/rep server and listen for such commands.
Commands sent to non-leader willl all return leader value
'''

class ClientMessage(object):
    # Types
    Leader = 0
    Append = 1

    def __init__(self, sender, receiver_host, receiver_port, command):
        self._snd_id = sender
        self._rcv_host = receiver_host
        self._rcv_port = receiver_port
        self._command = command

    @property
    def command(self):
        return self._command

    @property
    def sender(self):
        return self._snd_id

    @property
    def receiver_host(self):
        return self._receiver_host

    @property
    def receiver_port(self):
        return self._receiver_port

class ClientResponse(object):
    def __init__(self, receiver, leader, response):
        self._rcv_id = receiver
        self._leader_id = leader
        self._response = response

    @property
    def receiver(self):
        return self._rcv_id

    @property
    def leader(self):
        return self._leader_id

    @property
    def response(self):
        return self._response

class ClientFollowerResponse(ClientResponse):
    def __init__(self, receiver_id, leader_id):
        super(ClientFollowerResponse, self).__init__(receiver_id, leader_id, False)

class ClientLeaderResponse(ClientResponse):
    def __init__(self, receiver_id, leader_id, response):
        super(ClientLeaderResponse, self).__init__(receiver_id, leader_id, response)
