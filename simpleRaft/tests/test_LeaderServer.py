import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.append_entries import AppendEntriesMessage
from ..messages.request_vote import RequestVoteMessage
from ..servers.server import Server
from ..states.follower import Follower
from ..states.candidate import Candidate
from ..states.leader import Leader

class TestLeaderServer( unittest.TestCase ):

	def setUp( self ):

		followers = []
		for i in range( 1, 4 ):
			board = MemoryBoard()
			state = Follower()
			followers.append( Server( i, state, [], board, [] ) )

		board = MemoryBoard()
		state = Leader()
		
		self.leader = Server( 0, state, [], board, followers )

		for i in followers:
			i._neighbors.append( self.leader )

	def _perform_hearbeat( self ):
		self.leader._state._send_heart_beat()
		for i in self.leader._neighbors:
			i.on_message( i._messageBoard.get_message() )

		for i in self.leader._messageBoard._board:
			self.leader.on_message( i )

	def test_leader_server_sends_heartbeat_to_all_neighbors( self ):

		self._perform_hearbeat()
		self.assertEquals( { 1: 0, 2: 0, 3: 0 }, self.leader._state._nextIndexes ) 

	def test_leader_server_sends_appendentries_to_all_neighbors_and_is_appended_to_their_logs( self ):

		self._perform_hearbeat()

		msg = AppendEntriesMessage( 0, None, 1, { 
							"prevLogIndex": 0, 
							"prevLogTerm": 0, 
							"leaderCommit": 1, 
							"entries": [ { "term": 1, "value": 100 } ] } )

		self.leader.send_message( msg )

		for i in self.leader._neighbors:
			i.on_message( i._messageBoard.get_message() )

		for i in self.leader._neighbors:
			self.assertEquals( [{ "term": 1, "value": 100 } ], i._log )


	def test_leader_server_sends_appendentries_to_all_neighbors_but_some_have_dirtied_logs( self ):

		self.leader._neighbors[0]._log.append( { "term": 2, "value": 100 } )
		self.leader._neighbors[0]._log.append( { "term": 2, "value": 200 } )
		self.leader._neighbors[1]._log.append( { "term": 3, "value": 200 } )
		self.leader._log.append( { "term": 1, "value": 100 } )

		self._perform_hearbeat()

		msg = AppendEntriesMessage( 0, None, 1, { 
							"prevLogIndex": 0, 
							"prevLogTerm": 0, 
							"leaderCommit": 1, 
							"entries": [ { "term": 1, "value": 100 } ] } )

		self.leader.send_message( msg )

		for i in self.leader._neighbors:
			i.on_message( i._messageBoard.get_message() )

		for i in self.leader._neighbors:
			self.assertEquals( [{ "term": 1, "value": 100 } ], i._log )
			

