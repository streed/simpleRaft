import redis


class GossipingBoard( Board ):
  """This will connect to the local gossiping daemon and post and
  get messages from that daemon."""
