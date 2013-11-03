
from .state import State

from ..messages.request_vote import RequestVoteResponseMessage

class Voter( State ):

	def on_vote_request( self, message ):

		if( self._last_vote == None ):
			self._last_vote = message.sender
			self._send_vote_response_message( message )
		else:
			self._send_vote_response_message( message, yes=False )

		return self, None


	def _send_vote_response_message( self, msg, yes=True ):
		voteResponse = RequestVoteResponseMessage( self._server._name, msg.sender, msg.term, { "response": yes } )
		self._server.send_message_response( voteResponse )

