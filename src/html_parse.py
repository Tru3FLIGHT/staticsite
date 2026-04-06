from blocks import *
from extractors import extract_markdown_heading, extract_markdown_ordered_list
from htmlnode import HTMLNode
from inlines import text_to_TextNode
from leafnode import LeafNode
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
            div_children.append(node)
        else:
            first_fence_start = block.find("```")
            second_fence_start = block.find("```", first_fence_start + 3)

            if first_fence_start != -1 and second_fence_start != -1 and first_fence_start != second_fence_start:
                content_start = first_fence_start + 3
                # If there's a newline immediately after the opening fence, skip it.
                if content_start < len(block) and block[content_start] == '\n':
                    content_start += 1

                content_end = second_fence_start
                code_content = block[content_start:content_end]
                node = LeafNode("code", code_content)
            else:
                # Fallback for malformed blocks, though markdown_to_block should ideally prevent this.
                # If fences are not found as expected, strip all '```' and then any remaining whitespace.
                node = LeafNode("code", block.strip("```").strip())
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
            block = block.replace("\n", " ")
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
            lines = block.split('\n')
            stripped_lines = [line.lstrip('> ').strip() for line in lines]
            block = '\n'.join(stripped_lines)
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


