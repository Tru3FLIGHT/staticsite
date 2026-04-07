# Project Documentation

This document provides an overview of the functions within the `src` directory of the project.

## src/textnode.py

-   `TextNode(text: str, text_type: TextType, url=None)`
    Initializes a TextNode object with given text, text type, and an optional URL.
-   `__eq__(self, value: object, /) -> bool`
    Compares two `TextNode` objects for equality based on their text, text type, and URL.
-   `__repr__(self) -> str`
    Returns a string representation of the `TextNode` object for debugging.

## src/enums.py

This file defines various enumerations and constants used throughout the project.

-   `STATIC_PATH`: Constant for the static files directory.
-   `PUBLIC_PATH`: Constant for the public output directory.
-   `CONTENT_PATH`: Constant for the markdown content directory.
-   `TEMPLATE`: Constant for the HTML template file name.
-   `Split(Enum)`: An enumeration for different splitting mechanisms (e.g., `LINK`, `IMAGE`).
-   `BlockType(Enum)`: An enumeration for different types of markdown blocks (e.g., `PARAGRAPH`, `HEADING`, `CODE`, `QUOTE`, `U_LIST`, `O_LIST`).
-   `TextType(Enum)`: An enumeration for different types of text formatting (e.g., `TEXT`, `ITALIC`, `BOLD`, `CODE`, `LINK`, `IMAGE`).


## src/html_parse.py

-   `text_node_to_leaf(node: TextNode) -> LeafNode`
    Converts a `TextNode` object into a `LeafNode` object, mapping `TextType` to appropriate HTML tags.
-   `markdown_to_html_node(markdown: str) -> HTMLNode`
    Parses a markdown string and converts it into a hierarchical `HTMLNode` structure, representing the HTML content.
-   `text_to_children(block:str, block_type:BlockType) -> ParentNode`
    Converts a raw text block and its determined `BlockType` into a `ParentNode` containing corresponding `LeafNode` children.
-   `text_nodes_to_leaf_nodes(nodes:list[TextNode]) -> list[LeafNode]`
    Iterates through a list of `TextNode` objects and converts each one into a `LeafNode`.
-   `heading_count(block:str)`
    Determines the heading level (h1 to h6) of a markdown heading block by counting the '#' characters.
-   `list_to_html(block:str, block_type:BlockType)-> list[HTMLNode]`
    Converts a markdown list block (ordered or unordered) into a list of `HTMLNode` objects, typically `<li>` elements wrapped in `<ol>` or `<ul>`.


## src/blocks.py

-   `markdown_to_block(markdown: str) -> list[str]`
    Splits a raw markdown string into a list of distinct markdown blocks, typically separated by double newlines.
-   `block_to_block_type(block: str) -> BlockType`
    Analyzes a given markdown block and returns its corresponding `BlockType` (e.g., paragraph, heading, code, quote, list).


## src/parentnode.py

-   `ParentNode(tag, children:list, props=None)`
    Initializes a `ParentNode` object, which can contain other `HTMLNode` children.
-   `to_html(self)`
    Renders the `ParentNode` and all its children into a complete HTML string.


## src/leafnode.py

-   `LeafNode(tag, value, props=None)`
    Initializes a `LeafNode` object, representing a single HTML element with content but no children.
-   `__repr__(self) -> str`
    Returns a string representation of the `LeafNode` object for debugging.
-   `to_html(self) -> str`
    Renders the `LeafNode` into its corresponding HTML string representation.


## src/main.py

-   `main() -> None`
    The main entry point of the static site generator. It orchestrates the copying of static files and the generation of content pages.


## src/sitegen.py

-   `copy_static(source: str, destination: str, dest_clear:bool=False)`
    Recursively copies files and subdirectories from a source path to a destination path. It can optionally clear the destination directory before copying.


## src/extractors.py

-   `extract_markdown_image(text:str) -> list[tuple]`
    Extracts all markdown image syntax (e.g., `![alt text](url)`) from a given text, returning a list of tuples containing (alt text, url).
-   `extract_markdown_link(text:str) -> list[tuple]`
    Extracts all markdown link syntax (e.g., `[link text](url)`) from a given text, excluding images, returning a list of tuples containing (link text, url).
-   `extract_markdown_heading(text:str) -> list`
    Extracts markdown heading markers (e.g., `#`, `##`) from the beginning of a text string.
-   `extract_markdown_ordered_list(text:str) -> list`
    Extracts markdown ordered list markers (e.g., `1. `, `2. `) from a given text, considering multiple lines.


## src/inlines.py

-   `text_to_TextNode(text: str) -> list[TextNode]`
    Converts a raw text string into a list of `TextNode` objects by processing inline markdown for links, images, bold, italic, and code.
-   `split_nodes(old_nodes:list[TextNode], a: Split) -> list[TextNode]`
    Splits a list of `TextNode` objects based on whether they contain markdown links or images, creating new `TextNode` objects for the split parts.
-   `split_nodes_delimiter(old_nodes:list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]`
    Splits `TextNode` objects based on a specified delimiter (e.g., `**`, `_`, `` ` ``) and assigns a new `TextType` to the delimited content.


## src/pagegen.py

-   `extract_title(markdown:str) -> str`
    Extracts the main H1 title from a markdown string. Throws an exception if no H1 title is found.
-   `generate_page(source:str, template:str, destination:str, basepath = "/")`
    Generates a single HTML page from a markdown source file and an HTML template, writing the output to the specified destination. It also handles basepath replacements for links and images.
-   `gen_content(content_dir:str, template:str, destination:str, basepath = "/")`
    Recursively processes a content directory, generating HTML pages from all markdown files found within it and its subdirectories.
