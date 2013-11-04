from collections import defaultdict
from .state import State
from ..messages.append_entries import AppendEntriesMessage

class Leader( State ):

	def __init__( self ):
		self._nextIndexes = defaultdict(int)
		self._matchIndex = defaultdict(int)

	def set_sever( self, server ):
		self._sever = server
		self._send_heart_beat()
		
		for n in self._server._neighbors:
			self._nextIndexes[n._name] = self._server._lastLogIndex + 1
			self._matchIndex[n._name] = 0


	def on_response_received( self, message ):
		#Was the last AppendEntries good?
		if( not message.data["response"] ):
			#No, so lets back up the log for this node
			self._nextIndexes[message.sender] -= 1
			
			#Get the next log entry to send to the client.
			previousIndex = max( 0, self._nextIndexes[message.sender] - 1 )
			previous = self._server._log[prevLogIndex]
			current = self._server._log[self._nextIndexes[message.sender]]
			
			#Send the new log to the client and wait for it to respond.
			appendEntry = AppendEntriesMessage( self._server._name,
							message.sender,
							self._server._currentTerm,
							{
								"leaderId": self._server._name,
								"prevLogIndex": previousIndex,
								"prevLogTerm": previous["term"],
								"entries": [ current ],
								"leaderCommit": self._server._commitIndex
							})

			self._send_response_message( appendEntry )
		else:
			#The last append was good so increase their index.
			self._nextIndexes[message.sender] += 1

			#Are they caught up?
			if( self._nextIndexes[message.sender] > self._server._lastLogIndex ):
				self._nextIndexes[message.sender] = self._server._lastLogIndex

		return self, None 

	def _send_heart_beat( self ):
		message = AppendEntriesMessage( self._server._name, 
					 None, 
					 self._server._currentTerm, 
					 { 
						"leaderId": self._server._name,
					   	"prevLogIndex": self._server._lastLogIndex,
						"prevLogTerm": self._server._lastLogTerm,
						"entries": [],
						"leaderCommit": self._server._commitIndex 
					 })
		self._server.send_message( message )
