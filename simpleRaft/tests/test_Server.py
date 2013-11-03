import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.append_entries import AppendEntriesMessage
from ..servers.server import Server
from ..states.follower import Follower

class TestServer( unittest.TestCase ):

	def setUp( self ):
		board = MemoryBoard()
		state = Follower()
		self.server = Server( "test", state, [], board, [] )

	def test_server_on_message( self ):
		msg = AppendEntriesMessage( 0, 1, 2, {} )
		self.server.on_message( msg )

	def test_server_on_receive_message_with_greater_term( self ):

		msg = AppendEntriesMessage( 0, 1, 2, {} )

		self.assertEquals( 0, self.server._currentTerm )

		self.server.on_message( msg )

		self.assertEquals( 2, self.server._currentTerm )
