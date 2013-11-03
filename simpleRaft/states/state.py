
class State( object ):

	def on_message( self, message ):
		"""
			This method is called when a message is received,
			and calls one of the other corrosponding methods
			that this state reacts to.
		"""	

	def on_leader_timeout( self, message ):
		"""
			This is called when the leader timeout is reached.
		"""

	def on_vote_request( self, message ):
		"""
			This is called when there is a vote request.
		"""

	def on_vote_received( self, message ):
		"""
			This is called when this node recieves a vote.
		"""

	def on_append_entries( self, message ):
		"""
			This is called when there is a request to
			append an entry to the log.
		"""

	def on_client_command( self, message ):
		"""
			This is called when there is a client request.
		"""
