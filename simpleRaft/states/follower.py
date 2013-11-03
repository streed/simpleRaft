import time
import random

from .state import State
from ..messages.base import BaseMessage
from ..messages.response import ResponseMessage
from ..messages.request_vote import RequestVoteResponseMessage

class Follower( State ):

	def __init__( self, timeout=500 ):
		self._timeout = timeout
		self._timeoutTime = self._nextTimeout()
		self._last_vote = None

	def set_server( self, server ):
		self._server = server

	def _nextTimeout( self ):
		self._currentTime = time.time()
		return self._currentTime + random.randrange( self._timeout, 2 * self._timeout )

	def on_message( self, message ):
		_type = message.type

		if( message.term > self._server._currentTerm ):
			self._server._currentTerm = message.term

		if( _type == BaseMessage.AppendEntries ):
			return self.on_append_entries( message )
		elif( _type == BaseMessage.RequestVote ):
			return self.on_vote_request( message )


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
				else:
					#The commit index is not out of the range of the log
					#So we can just append it to the log now.
					#commitIndex = len( log )
					log.append( data["commitValue"] )
					self._server._commitIndex += 1


			self._send_response_message( message )
			return self, None
		else:
			return self, None

	def on_vote_request( self, message ):

		if( self._last_vote == None ):
			self._last_vote = message.sender
			self._send_vote_response_message( message )
		else:
			self._send_vote_response_message( message, yes=False )

		return self, None

	def _send_response_message( self, msg, yes=True ):
		response = ResponseMessage( self._server._name, msg.sender, msg.term, { "response": yes } )
		self._server.send_message_response( response )

	def _send_vote_response_message( self, msg, yes=True ):
		voteResponse = RequestVoteResponseMessage( self._server._name, msg.sender, msg.term, { "response": yes } )
		self._server.send_message_response( voteResponse )

