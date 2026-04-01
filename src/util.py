import re
from leafnode import LeafNode
from textnode import TextNode, TextType


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
