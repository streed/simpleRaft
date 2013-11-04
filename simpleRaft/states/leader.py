from .state import State

class Leader( State ):

	def set_sever( self, server ):
		self._sever = server
		self._send_heart_beat()

	def _send_heart_beat( self ):
		message = AppendEntries( self._server._name, None, self._server._currentTerm, { "leaderId": self._server._name,
												"prevLogIndex": self._server._lastLogIndex,
												"prevLogTerm": self._server._lastLogTerm,
												"entries": [],
												"leaderCommit": self._server._commitIndex })
		self._server.send_message( message )
