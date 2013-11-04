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


	def test_leader_server_sends_heartbeat_to_all_neighbors( self ):

		self.leader._state._send_heart_beat()

		for i in self.leader._neighbors:
			i.on_message( i._messageBoard.get_message() )

		for i in self.leader._messageBoard._board:
			self.leader.on_message( i )

		self.assertEquals( { 1: 0, 2: 0, 3: 0 }, self.leader._state._nextIndexes ) 
