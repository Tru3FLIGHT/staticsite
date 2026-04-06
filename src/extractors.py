import re

def extract_markdown_image(text:str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_link(text:str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_heading(text:str) -> list:
    return re.findall(r"^(#{1,6})\s", text)

def extract_markdown_ordered_list(text:str) -> list:
    return re.findall(r"^(\d+\.\s)", text, re.MULTILINE)
