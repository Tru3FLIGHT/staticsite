from blocks import *
from extractors import extract_markdown_heading
from htmlnode import HTMLNode
from inlines import text_to_TextNode
from leafnode import LeafNode
from parentnode import ParentNode
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

# def markdown_to_html(markdown: str) -> HTMLNode:
#     blocks = markdown_to_block(markdown)
#     children: list[HTMLNode] = []
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         if block_type != BlockType.CODE:
#             tag = determine_tag(block_type, block)
#             list_of_children = text_to_children(block, block_type)
#             children.append(ParentNode(determine_tag(block_type), list_of_children))
#         else:
#             children.append(text_node_to_leaf(TextNode(block, TextType.CODE)))


def text_to_children(block: str, blocktype: BlockType) -> list[HTMLNode]:
    textnodes = text_to_TextNode(block)
    children = []
    for node in textnodes:
        child = text_node_to_leaf(node)
        children.append(child)
    return children


def determine_tag(block_type: BlockType, block: str):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return extract_markdown_heading(block)[0].count('#')
