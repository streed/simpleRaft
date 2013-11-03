import time
import random

from .state import State
from ..messages.base import BaseMessage

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
			return follow, None
		

		if( message.data != {} ): 
			log = self._server._log
			data = message.data
			if( len( log ) < data["prevLogIndex"] )
				self._send_response_message( message, yes=False )
				return self, None

			elif( log[data["prevLogIndex"]] != None ):
				self._send_response_message( message, yes=False )
				return self, None

			elif( log[data["prevLogIndex"]] != data["prevLogTerm"] ):
				log = log[:data["prevLogIndex"]]
				self._send_response_message( message )
				return self, None
			else:
				log.append( data["logTerm"] )

			if( data["leaderCommitIndex"] > self._server._commitIndex ):
				self._server._commitIndex = min( data["leaderCommitIndex"], len( log ) )


			self._send_response_message( message )
			return self, None
		else:
			return self, None

	def on_vote_request( self, message ):

		if( self._lst_vote == None ):
			self._last_vote = message.sender
			self._send_vote_response_message( message )
		else:
			self._send_vote_response_message( message, yes=False )

	def _send_response_message( self, msg, yes=True )
		response = ResponseMessage( self._name, msg.sender, msg.term, { "response": yes } )
		self._server.send_message_response( response )

	def _send_vote_response_message( self, msg, yes=True ):
		voteResponse = VoteResponseMessage( self._name, message.sender, message.term, { "response": yes } )
		self._server.send_message_response( voteResponse )

