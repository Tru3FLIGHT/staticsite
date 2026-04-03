import re
from enum import Enum
from leafnode import LeafNode
from textnode import TextNode, TextType

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

RULES = [
    (BlockType.CODE, re.compile(r"^```[\s\S]*?```$", re.MULTILINE)),
    (BlockType.HEADING, re.compile(r"^\s{0,3}#{1,6}\s")),
    (BlockType.O_LIST, re.compile(r"^\s*\d+\.\s")),
    (BlockType.U_LIST, re.compile(r"^\s*[-*+]\s")),
    (BlockType.QUOTE, re.compile(r"^\s*>\s")),
]



def markdown_to_block(markdown: str) -> list[str]:
    out = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            out.append(block)
    return out

def block_to_block_type(block: str) -> BlockType:
    for block_type, pattern in RULES:
        if pattern.search(block):
            return block_type
    return BlockType.PARAGRAPH


def text_to_TextNode(text: str) -> list[TextNode]:
    out = []
    out = split_nodes([TextNode(text, TextType.TEXT)], Split.LINK)
    out = split_nodes(out, Split.IMAGE)
    out = split_nodes_delimiter(out, "**", TextType.BOLD)
    out = split_nodes_delimiter(out, "_", TextType.ITALIC)
    out = split_nodes_delimiter(out, "`", TextType.CODE)
    return out

def split_nodes(old_nodes:list[TextNode], a: Split) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
            continue
        instances = extract_markdown_link(node.text) if a == Split.LINK else extract_markdown_image(node.text)
        if len(instances) == 0:
            out.append(node)
            continue
        current_text = node.text
        for i in range(0, len(instances)):
            instance = instances[i]
            segment = current_text.split(f"[{instance[0]}]({instance[1]})",1) if a == Split.LINK else current_text.split(f"![{instance[0]}]({instance[1]})")
            out.append(TextNode(segment[0], TextType.TEXT))
            out.append(TextNode(instance[0], TextType.LINK if a == Split.LINK else TextType.IMAGE, instance[1]))
            if i == len(instances)-1 and segment[1] != "":
                out.append(TextNode(segment[1], TextType.TEXT))
                break
            current_text = segment[1]
    return out


def text_node_to_leaf(node: TextNode) -> LeafNode:

        match node.text_type:
            case TextType.TEXT:
                return LeafNode(None, node.text)
            case TextType.BOLD:
                return LeafNode("b", node.text)
            case TextType.ITALIC:
                return LeafNode("i", node.text)
            case TextType.CODE:
                return LeafNode("code", node.text)
            case TextType.LINK:
                if node.url:
                    return LeafNode("a", node.text, {"href":node.url})
                raise ValueError(f"{node} has no attribute url")
            case TextType.IMAGE:
                if node.url:
                    return LeafNode("img", "", {"src":node.url, "alt":node.text})
                raise ValueError(f"{node} has no attribute url")
            case _:
                raise ValueError(f"{node}, does not have valid TextType {node.text_type}")


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            out.append(node)
            continue
        texts = node.text.split(delimiter)
        if len(texts) % 2 != 1:
            raise ValueError(f"Invalid markdown syntax: {node.text}")
        for i in range(0, len(texts)):
            if i % 2 == 0:
                if texts[i] != "":
                    out.append(TextNode(texts[i], TextType.TEXT))
            else:
                out.append(TextNode(texts[i], text_type))
    return out


def extract_markdown_image(text:str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_link(text:str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
