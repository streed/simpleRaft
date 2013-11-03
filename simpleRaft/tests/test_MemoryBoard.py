import unittest

from ..boards.memory_board import MemoryBoard
from ..messages.base import BaseMessage

class TestMemoryBoard( unittest.TestCase ):

	def setUp( self ):
		self.board = MemoryBoard()

	def test_memoryboard_post_message( self ):

		msg = BaseMessage( 0, 0, 0, 0 )	
		self.board.post_message( msg )
		self.assertEquals( msg, self.board.get_message() )

	def test_memoryboard_post_message( self ):

		msg = BaseMessage( 0, 0, 0, 0 )
		msg2 = BaseMessage( 0, 0, 0, 0 )
		msg2._timestamp -= 100
	
		self.board.post_message( msg )
		self.board.post_message( msg2 )

		self.assertEquals( msg2, self.board.get_message() )

