from enum import Enum


STATIC_PATH = "static/"
PUBLIC_PATH = "docs/"
CONTENT_PATH = "content/"
TEMPLATE = "template.html"


class Split(Enum):
    LINK = "link"
    IMAGE = "image" 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered list"
    O_LIST = "ordered list"

class TextType(Enum):
    TEXT = "plain text"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


