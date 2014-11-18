from .base import BaseMessage


class ResponseMessage(BaseMessage):

    _type = BaseMessage.Response

    def __init__(self, sender, receiver, term, data):
        BaseMessage.__init__(self, sender, receiver, term, data)
