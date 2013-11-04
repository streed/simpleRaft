import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.append_entries import AppendEntriesMessage
from ..messages.request_vote import RequestVoteMessage
from ..servers.server import Server
from ..states.follower import Follower
from ..states.candidate import Candidate

class TestCandidateServer( unittest.TestCase ):

	def setUp( self ):
		board = MemoryBoard()
		state = Follower()
		self.oserver = Server( 0, state, [], board, [] )

		board = MemoryBoard()
		state = Candidate()
		self.server = Server( 1, state, [], board, [ self.oserver ] )

		self.oserver._neighbors.append( self.server )

	def test_candidate_server_had_intiated_the_election( self ):

		self.assertEquals( 1, len( self.oserver._messageBoard._board ) )

		self.oserver.on_message( self.oserver._messageBoard.get_message() )

		self.assertEquals( 1, len( self.server._messageBoard._board ) )
		self.assertEquals( True, self.server._messageBoard.get_message().data["response"] )

	def test_candidate_server_had_gotten_the_vote( self ):
		self.oserver.on_message( self.oserver._messageBoard.get_message() )

		self.assertEquals( 1, len( self.server._messageBoard._board ) )
		self.assertEquals( True, self.server._messageBoard.get_message().data["response"] )

	def test_candidate_server_wins_election( self ):
		board = MemoryBoard()
		state = Follower()
		server0 = Server( 0, state, [], board, [] )

		board = MemoryBoard()
		state = Follower()
		oserver = Server( 1, state, [], board, [] )

		board = MemoryBoard()
		state = Candidate()
		server = Server( 2, state, [], board, [ oserver, server0 ] )

		server0._neighbors.append( server )
		oserver._neighbors.append( server )

		oserver.on_message( oserver._messageBoard.get_message() )
		server0.on_message( server0._messageBoard.get_message() )

		server.on_message( server._messageBoard.get_message() )
		server.on_message( server._messageBoard.get_message() )
