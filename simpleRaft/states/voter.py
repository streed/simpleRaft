from .state import State

from ..messages.request_vote import RequestVoteResponseMessage
from ..messages.client import ClientFollowerResponse

class Voter(State):

    def __init__(self, timeout=1.0):
        super(Voter, self).__init__(timeout=timeout)
        self._last_vote = None

    def on_vote_request(self, message):
        if(self._last_vote is None and
           message.data["lastLogIndex"] >= self._server._lastLogIndex):
            self._last_vote = message.sender
            self._send_vote_response_message(message)
        else:
            self._send_vote_response_message(message, yes=False)

        return self, None

    def _send_vote_response_message(self, msg, yes=True):
        voteResponse = RequestVoteResponseMessage(
            self._server._name,
            msg.sender,
            msg.term,
            {"response": yes})
        self._server.send_message_response(voteResponse)
    
    def on_client_message(self, message):
        ''' return the message response for the client '''
        return ClientFollowerResponse(message.sender, self._last_vote)
