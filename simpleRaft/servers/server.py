
class Server( object ):

	def __init__( self, name, state, log, messageBoard, neighbors ):
		self._name = name
		self._state = state
		self._log = log
		self._messageBoard = messageBoard
		self._neighbors = neighbors

		self._commitIndex = 0
		self._currentTerm = 0
		
		self._lastLogIndex = 0
		self._lastLogTerm = None

		self._state.set_server( self )
		self._messageBoard.set_owner( self )

	def send_message( self, message ):
		for n in self._neighbors:
			message._receiver = n._name
			n.post_message( message )

	def send_message_response( self, message ):
		n = [ n for n in self._neighbors if n._name == message.receiver ]
		if( len( n ) > 0 ):
			n[0].post_message( message )

	def post_message( self, message ):
		self._messageBoard.post_message( message )

	def on_message( self, message ):
		state, response = self._state.on_message( message )

		self._state = state
