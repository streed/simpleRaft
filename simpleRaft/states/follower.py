from .voter import Voter
from ..messages.base import BaseMessage
from ..messages.response import ResponseMessage

class Follower( Voter ):

	def __init__( self, timeout=500 ):
		Voter.__init__( self )
		self._timeout = timeout
		self._timeoutTime = self._nextTimeout()

	def on_append_entries( self, message ):
		self._timeoutTime = self._nextTimeout()

		if( message.term < self._server._currentTerm ):
			self._send_response_message( message, yes=False )
			return self, None
		
		if( message.data != {} ): 
			log = self._server._log
			data = message.data

			#Check if the leader is too far ahead in the log.
			if( data["leaderCommitIndex"] > self._server._commitIndex ):
				#If the leader is too far ahead then we use the length of the log - 1
				self._server._commitIndex = min( data["leaderCommitIndex"], len( log ) - 1 )

			if( "prevLogIndex" in data and len( log ) < data["prevLogIndex"] ):
				self._send_response_message( message, yes=False )
				return self, None

			#We need to hold the induction proof of the algorithm here.
			#So, we make sure that the prevLogIndex term is always
			#equal to the server.
			if( "prevLogIndex" in data and log[data["prevLogIndex"]] != data["prevLogTerm"] ):
				log = log[:data["prevLogIndex"] + 1]
				log[data["prevLogIndex"]] = data["prevLogTerm"]
				self._send_response_message( message )
				self._server._log = log
				self._server._lastLogIndex = data["prevLogIndex"]
				self._server._lastLogValue = data["prevLogTerm"]
				return self, None
			#The induction proof held so lets check if the commitIndex 
			#value is the same as the one on the leader
			else:
				#Make sure that leaderCommitIndex is > 0 and that the data is different here
				if( data["leaderCommitIndex"] > 0 and log[data["leaderCommitIndex"]] != data["commitValue"] ):	
					#Data was found to be different so we fix that
					#By taking the current log and slicing it to the leaderCommitIndex + 1 range
					#Then setting the last value to the commitValue
					log = log[:data["leaderCommitIndex"] + 1]
					log[data["leaderCommitIndex"]] = data["commitValue"]
					self._send_response_message( message )
					self._server._log = log
					self._server._lastLogIndex = data["leaderCommitIndex"]
					self._server._lastLogValue = data["commitValue"]
				else:
					#The commit index is not out of the range of the log
					#So we can just append it to the log now.
					#commitIndex = len( log )
					log.append( data["commitValue"] )
					self._server._commitIndex += 1
					self._server._lastLogIndex = len( log ) - 1
					self._server._lastLogValue = log[:-1]
					self._commitIndex = len( log ) - 1


			self._send_response_message( message )
			return self, None
		else:
			return self, None

