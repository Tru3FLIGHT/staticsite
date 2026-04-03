from enums import TextType, Split
from textnode import TextNode
from extractors import *

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

