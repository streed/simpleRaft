from collections import defaultdict
from .voter import Voter
from ..messages.append_entries import AppendEntriesMessage
from ..messages.client import ClientMessage, ClientLeaderResponse


class Leader(Voter):

    def __init__(self, timeout=1.0):
        super(Leader, self).__init__(timeout=timeout)
        self._nextIndexes = defaultdict(int)
        self._matchIndex = defaultdict(int)
        self._last_heartbeat = 0

    def set_server(self, server):
        self._server = server

        for n in self._server._neighbors:
            self._nextIndexes[n._name] = self._server._lastLogIndex + 1
            self._matchIndex[n._name] = 0

    def on_append_entries(self, message):
        if message.sender == self._server._name:
            # bcast
            return self, None
        if message.term > self._server._currentTerm:
            ## If we're getting append messages from the future, we're not the leader
            from .follower import Follower
            follower = Follower()
            follower.set_server(self._server)
            return follower, None
        raise RuntimeError

    def on_vote_received(self, message):
        ''' Well I find it dandy you're still voting for me '''
        return self, None

    def on_response_received(self, message):
        # Was the last AppendEntries good?
        if(not message.data["response"]):
            # No, so lets back up the log for this node
            self._nextIndexes[message.sender] -= 1

            # Get the next log entry to send to the client.
            previousIndex = max(0, self._nextIndexes[message.sender] - 1)
            previous = self._server._log[previousIndex]
            current = self._server._log[self._nextIndexes[message.sender]]

            # Send the new log to the client and wait for it to respond.
            appendEntry = AppendEntriesMessage(
                self._server._name,
                message.sender,
                self._server._currentTerm,
                {
                    "leaderId": self._server._name,
                    "prevLogIndex": previousIndex,
                    "prevLogTerm": previous["term"],
                    "entries": [current],
                    "leaderCommit": self._server._commitIndex,
                })

            self._send_response_message(appendEntry)
        else:
            # The last append was good so increase their index.
            self._nextIndexes[message.sender] += 1

            # Are they caught up?
            if(self._nextIndexes[message.sender] > self._server._lastLogIndex):
                self._nextIndexes[message.sender] = self._server._lastLogIndex

        return self, None

    @property
    def timeout(self):
        ''' Nyquist rate on avg election timeout; bcast freq >= 3x timeout freq ==> no timeouts '''
        return self._timeout * .75

    def on_leader_timeout(self):
        ''' While leader, bcast heartbeat on timeout '''
        self._send_heart_beat()
        return self, None

    def _send_heart_beat(self):
        message = AppendEntriesMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "leaderId": self._server._name,
                "prevLogIndex": self._server._lastLogIndex,
                "prevLogTerm": self._server._lastLogTerm,
                "entries": [],
                "leaderCommit": self._server._commitIndex,
            })
        self._server.send_message(message)

    def on_client_message(self, message):
        if message.command == ClientMessage.Leader:
            return ClientLeaderResponse(message.sender, self._server._name, True)
        else:
            #TODO: Raft lol
            raise NotImplemented
