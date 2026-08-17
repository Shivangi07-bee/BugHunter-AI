class GraphNode:

    def __init__(self, node_id, node_type, data):

        self.id = node_id
        self.type = node_type
        self.data = data

    def to_dict(self):

        return {
            "id": self.id,
            "type": self.type,
            "data": self.data
        }