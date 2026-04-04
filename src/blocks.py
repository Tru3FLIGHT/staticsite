from enums import BlockType
import re


RULES = [
    (BlockType.CODE, re.compile(r"^```[\s\S]*?```$", re.MULTILINE)),
    (BlockType.HEADING, re.compile(r"^#{1,6}\s")),
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

