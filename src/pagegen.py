import os
from html_parse import heading_count, markdown_to_html_node
from blocks import markdown_to_block, block_to_block_type
from enums import BlockType

def extract_title(markdown:str) -> str:
    blocks = markdown_to_block(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if heading_count(block) == 1:
                return block.strip("# \n")
    raise Exception(f"input markdown contains no h1 title heading block")

def generate_page(source:str, template:str, destination:str):
    print(f"generating page from {source} to {destination} using {template}")
    with open(source) as f:
        markdown = f.read()
    with open(template) as f:
        temp_content = f.read()
    file_node = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    cont = temp_content.replace("{{ Title }}", title)
    final = cont.replace("{{ Content }}", file_node)

    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))

    with open(destination, "w") as f:
        f.write(final)
    



