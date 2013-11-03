import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.append_entries import AppendEntriesMessage
from ..messages.request_vote import RequestVoteMessage
from ..servers.server import Server
from ..states.follower import Follower

class TestFollowerServer( unittest.TestCase ):

	def setUp( self ):
		board = MemoryBoard()
		state = Follower()
		self.oserver = Server( 0, state, [], board, [] )

		board = MemoryBoard()
		state = Follower()
		self.server = Server( 1, state, [], board, [ self.oserver ] )

	def test_follower_server_on_message( self ):
		msg = AppendEntriesMessage( 0, 1, 2, {} )
		self.server.on_message( msg )



	def test_follower_server_on_receive_message_with_lesser_term( self ):

		msg = AppendEntriesMessage( 0, 1, -1, {} )

		self.server.on_message( msg )

		self.assertEquals( False, self.oserver._messageBoard.get_message().data["response"] )

	def test_follower_server_on_receive_message_with_greater_term( self ):

		msg = AppendEntriesMessage( 0, 1, 2, {} )

		self.server.on_message( msg )

		self.assertEquals( 2, self.server._currentTerm )

	def test_follower_server_on_receive_message_where_log_does_not_have_prevLogTerm( self ):
		self.server._log.append( 2000 )
		msg = AppendEntriesMessage( 0, 1, 2, { "prevLogIndex": 0, "prevLogTerm": 100, "leaderCommitIndex": 1, "commitValue": 100 } )

		self.server.on_message( msg )

		self.assertEquals( True, self.oserver._messageBoard.get_message().data["response"] )
		self.assertEquals( 100, self.server._log[0] )

	def test_follower_server_on_receive_message_where_log_contains_conflicting_entry_at_new_index( self ):

		self.server._log.append( 100 )
		self.server._log.append( 200 )
		self.server._log.append( 300 )

		msg = AppendEntriesMessage( 0, 1, 2, { "prevLogIndex": 0, "prevLogTerm": 100, "leaderCommitIndex": 1, "commitValue": 100 } )

		self.server.on_message( msg )
		self.assertEquals( 100, self.server._log[1] )
		self.assertEquals( [ 100, 100 ], self.server._log )

	def test_follower_server_on_receive_message_where_log_is_empty_and_receives_its_first_value( self ):

		msg = AppendEntriesMessage( 0, 1, 2, { "leaderCommitIndex": 0, "commitValue": 100 } )

		self.server.on_message( msg )
		self.assertEquals( 100, self.server._log[0] )

	def test_follower_server_on_receive_vote_request_message( self ):
		msg = RequestVoteMessage( 0, 1, 2, {} )

		self.server.on_message( msg )

		self.assertEquals( 0, self.server._state._last_vote )
		self.assertEquals( True, self.oserver._messageBoard.get_message().data["response"] )

	def test_follower_server_on_receive_vote_request_after_sending_a_vote( self ):
		msg = RequestVoteMessage( 0, 1, 2, {} )

		self.server.on_message( msg )

		msg = RequestVoteMessage( 2, 1, 2, {} )
		self.server.on_message( msg )

		self.assertEquals( 0, self.server._state._last_vote )
