from .base import BaseMessage

class AppendEntriesMessage( BaseMessage ):
	
	_type = BaseMessage.AppendEntries

	def __init__( self, sender, receiver, term, data ):
		BaseMessage.__init__( self, sender, receiver, term, data )
