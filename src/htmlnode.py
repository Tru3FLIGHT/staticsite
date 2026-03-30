class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        out = ""
        if self.props is None:
            return out
        for element in self.props:
            out += f"{element}=\"{self.props[element]}\" "
        return out

