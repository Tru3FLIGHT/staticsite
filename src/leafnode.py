from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None) -> None:
        if value is None:
            raise ValueError("LeafNode.value cannot be None")
        super().__init__(tag, value, None, props)


    #TODO:Parcing language for html
    def to_html(self) -> str:
        out = ""
        if not self.value:
            raise ValueError("LeafNode must have value")
        if self.tag == None:
            return self.value

        return out
