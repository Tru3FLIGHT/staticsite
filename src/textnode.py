from enum import Enum

class TextType(Enum):
    TEXT = "plain text"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str, text_type: TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            raise AttributeError(f"{value.__class__} not implemented")
        if self.text != value.text:
            return False
        if self.text_type != value.text_type:
            return False
        if self.url != value.url:
            return False
        return True
        
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
