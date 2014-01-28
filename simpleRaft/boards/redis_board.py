import redis
from board import Board

class RedisBoard( Board ):
  """This will create a message board that is backed by Redis."""
  
  def __init__( self, *args, **kwargs ):
    """Creates the Redis connection."""
    self.redis = redis.Redis( *args, **kwargs )
    
  def set_owner( self, owner ):
    self.owner = owner
    
  def post_message( self, message ):
    """This will append the message to the list."""
    pass
    
  def get_message( self ):
    """This will pop a message off the list."""
    pass
    
  def _key( self ):
    if not self.key:
      self.key = "%s-queue" % self.owner
    
    return self.key
