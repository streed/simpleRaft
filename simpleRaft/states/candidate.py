from .voter import Voter
from .leader import Leader
from ..messages.request_vote import RequestVoteMessage

class Candidate( Voter ):

	def set_server( self, server ):
		self._server = server
		self._votes = {}
		self._start_election()

	def on_vote_request( self, message ):
		return self, None

	def on_vote_received( self, message ):
		if( not message.sender in self._votes ):
			self._votes[message.sender] = message

			if( len( self._votes.keys() ) > len( self._server._neighbors ) / 2 ):
				leader = Leader()
				leader.set_server( self._server )

				return leader, None
		return self, None


	def _start_election( self ):
		self._server._currentTerm += 1
		election = RequestVoteMessage( self._server._name, 
					    None, 
					    self._server._currentTerm, 
					    { 
						"lastLogIndex": self._server._lastLogIndex,
						"lastLogTerm": self._server._lastLogTerm })

		self._server.send_message( election )
		self._last_vote = self._server._name
