from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag, children:list, props=None) -> None:
        super().__init__(tag,None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("children in ParentNode cannot be None")
        out = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if child.value is None:
                raise ValueError(f"Error: {child} has no attribute Value")
            out += child.to_html()
        return out + f"</{self.tag}>"

