from blocks import *
from extractors import extract_markdown_heading, extract_markdown_ordered_list
from htmlnode import HTMLNode
from inlines import text_to_TextNode
from leafnode import LeafNode
import parentnode
from textnode import TextNode
from parentnode import ParentNode
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
                raise ValueError(f"{node}, does not have valid TextType {node.text_type}") #type: ignore

def markdown_to_html_node(markdown: str) -> HTMLNode:
    div_children = []
    blocks = markdown_to_block(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:
            node = text_to_children(block.strip(), block_type)
        else:
            node = LeafNode("code",block.strip().strip("```").strip())
            pre = ParentNode("pre", [node])
            div_children.append(pre)
    div = ParentNode("div", div_children)
    return div

def text_to_children(block:str, block_type:BlockType) -> ParentNode:
    tag = ""
    children = []
    match block_type:
        case BlockType.PARAGRAPH:
            tag = "p"
            nodes = text_to_TextNode(block)
            children.extend(text_nodes_to_leaf_nodes(nodes))
        case BlockType.O_LIST:
            tag = "ol"
            children.extend(list_to_html(block, block_type))
        case BlockType.U_LIST:
            tag = "ul"
            children.extend(list_to_html(block, block_type))
        case BlockType.HEADING:
            tag = f"h{heading_count(block)}"
            block = block.lstrip("# ")
            nodes = text_to_TextNode(block)
            children.extend(text_nodes_to_leaf_nodes(nodes))
        case BlockType.QUOTE:
            tag = "blockquote"
            nodes = text_to_TextNode(block)
            children.extend(text_nodes_to_leaf_nodes(nodes))
    return ParentNode(tag, children)

def text_nodes_to_leaf_nodes(nodes:list[TextNode]) -> list[LeafNode]:
    children = []
    for node in nodes:
        children.append(text_node_to_leaf(node))
    return children

def heading_count(block:str):
    return extract_markdown_heading(block)[0].count("#")

def list_to_html(block:str, block_type:BlockType)-> list[HTMLNode]:
    splits = []
    splitters = []
    if block_type == BlockType.U_LIST:
        for i in range(0,block.count("- ")):
            splitters.append("- ")
    else:
        splitters = extract_markdown_ordered_list(block)
    current_text = block
    for i in range(0, len(splitters)):
        splitter = splitters[i]
        segments = current_text.split(splitter, 1)
        if i != 0:
            splits.append(segments[0].strip())

        if i == len(splitters)-1:
            splits.append(segments[1].strip())
        current_text = segments[1]
    out: list[HTMLNode] = []
    for split in splits:
        nodes = text_to_TextNode(split)
        children = text_nodes_to_leaf_nodes(nodes)
        out.append(ParentNode("li",children))
    return out


