#!/usr/bin/python

import random

from ..messages.base import BaseMessage
from ..messages.response import ResponseMessage


class State(object):

    def __init__(self, timeout=1.0):
        self._timeout = timeout

    def set_server(self, server):
        self._server = server

    def on_message(self, message):
        """This method is called when a message is received,
        and calls one of the other corrosponding methods
        that this state reacts to.

        """
        _type = message.type
        # Convert to follower if heigher term received
        if(message.term > self._server._currentTerm):
            self._server._currentTerm = message.term
            from .follower import Follower
            if not issubclass(type(self), Follower):
                follower = Follower(timeout=self._timeout)
                follower.set_server(self._server)
                return follower.on_message(message)

        # Is the messages.term < ours? If so we need to tell
        #   them this so they don't get left behind.
        elif(message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if(_type == BaseMessage.AppendEntries):
            return self.on_append_entries(message)
        elif(_type == BaseMessage.RequestVote):
            return self.on_vote_request(message)
        elif(_type == BaseMessage.RequestVoteResponse):
            return self.on_vote_received(message)
        elif(_type == BaseMessage.Response):
            return self.on_response_received(message)

    def on_leader_timeout(self):
        """This is called when the leader timeout is reached."""
        raise NotImplemented

    def on_vote_request(self, message):
        """This is called when there is a vote request."""
        return self, None

    def on_vote_received(self, message):
        """This is called when this node recieves a vote."""
        return self, None

    def on_append_entries(self, message):
        """This is called when there is a request to
        append an entry to the log.
        """
        raise NotImplemented

    def on_response_received(self, message):
        """This is called when a response is sent back to the Leader"""
        return self, None

    def on_client_command(self, message):
        """This is called when there is a client request."""
        raise NotImplemented

    @property
    def timeout(self):
        return random.uniform(self._timeout, 2.0 * self._timeout)

    def _send_response_message(self, msg, yes=True):
        response = ResponseMessage(self._server._name, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self._server._currentTerm,
        })
        self._server.send_message_response(response)
