from .base import BaseMessage

class RequestVoteMessage( BaseMessage ):

	_type = BaseMessage.RequestVote

	def __init__( self, sender, receiver, term, data ):
		BaseMessage.__init__( self, sender, receiver, term, data )

class RequestVoteResponseMessage( BaseMessage ):

	_type = BaseMessage.RequestVote

	def __init__( self, sender, receiver, term, data ):
		BaseMessage.__init__( self, sender, receiver, term, data )
