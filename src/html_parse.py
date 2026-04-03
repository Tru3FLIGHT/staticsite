from blocks import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode
from enums import TextType, BlockType


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

def markdown_to_html(markdown: str) -> HTMLNode:
    blocks = markdown_to_block(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = make_htmlnode(block_type, block)

def make_htmlnode(blocktype: BlockType, block: str) -> HTMLNode:
    

def text_to_children(block):
