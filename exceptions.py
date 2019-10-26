class VisitedNodeError(Exception):
    def __init__(self, message):
        self.message = message


class NodeIsAlreadyVisited(Exception):
    def __init__(self, message):
        self.message = message
