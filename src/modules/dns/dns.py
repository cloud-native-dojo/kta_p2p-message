class Dns:  
    node_dict = {}
    
    @classmethod
    def get_node(cls, node_id: int):
        return cls.node_dict[node_id]
    
    @classmethod
    def add_node(cls, node):
        cls.node_dict[node.get_id()] = node


    
