from .voter import Voter
from ..messages.request_vote import RequestVoteMessage


class Candidate(Voter):

    def __init__(self, timeout=1.0):
        super(Candidate, self).__init__(timeout=timeout)
        self._last_heartbeat = 0

    def set_server(self, server):
        self._server = server

    def on_leader_timeout(self):
        ''' this event triggers an election '''
        self._votes = {}
        self._start_election()
        return self, None

    def on_vote_request(self, message):
        return self, None

    def on_vote_received(self, message):
        if message.sender not in self._votes:
            self._votes[message.sender] = message

            if(len(self._votes.keys()) > (self._server._total_nodes - 1) / 2):
                from .leader import Leader
                leader = Leader(timeout=self._timeout)
                leader.set_server(self._server)
                leader._last_vote = self._last_vote
                leader._send_heart_beat()
                return leader, None
        return self, None

    def on_append_entries(self, message):
        ''' revert to follower, call on_append_entries '''
        from .follower import Follower
        follower = Follower(timeout=self._timeout)
        follower.set_server(self._server)
        return follower.on_append_entries(message)

    def _start_election(self):
        self._server._currentTerm += 1
        election = RequestVoteMessage(
            self._server._name,
            None,
            self._server._currentTerm,
            {
                "lastLogIndex": self._server._lastLogIndex,
                "lastLogTerm": self._server._lastLogTerm,
            })

        self._server.send_message(election)
        self._last_vote = self._server._name
