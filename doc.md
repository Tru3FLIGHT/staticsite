# Project Documentation

This document provides an overview of the functions within this project.

---

## `src/textnode.py`

### `TextNode.__init__(self, text: str, text_type: TextType, url=None) -> None`
Initializes a TextNode object.
- `text`: The text content of the node.
- `text_type`: The type of text (e.g., plain, bold, italic).
- `url`: Optional URL for link or image text types.

### `TextNode.__eq__(self, value: object, /) -> bool`
Compares two TextNode objects for equality.
- `value`: The other TextNode object to compare with.
- Returns `True` if the text, text type, and URL are identical, `False` otherwise.
- Raises `AttributeError` if `value` is not a TextNode.

### `TextNode.__repr__(self) -> str`
Returns a string representation of the TextNode object.

---

## `src/enums.py`

### `class Split(Enum)`
An enumeration for splitting types.
- `LINK = "link"`
- `IMAGE = "image"`

### `class BlockType(Enum)`
An enumeration for different types of markdown blocks.
- `PARAGRAPH = "paragraph"`
- `HEADING = "heading"`
- `CODE = "code"`
- `QUOTE = "quote"`
- `U_LIST = "unordered list"`
- `O_LIST = "ordered list"`

### `class TextType(Enum)`
An enumeration for different types of text formatting.
- `TEXT = "plain text"`
- `ITALIC = "italic"`
- `BOLD = "bold"`
- `CODE = "code"`
- `LINK = "link"`
- `IMAGE = "image"`

---

## `src/htmlnode.py`

### `HTMLNode.__init__(self, tag=None, value=None, children=None, props=None) -> None`
Initializes an HTMLNode object.
- `tag`: The HTML tag name (e.g., "p", "a", "div").
- `value`: The raw HTML value if no children.
- `children`: A list of HTMLNode objects that are children of this node.
- `props`: A dictionary of HTML attributes (e.g., {"href": "https://www.google.com"}).

### `HTMLNode.to_html(self)`
Raises `NotImplementedError`. This method is intended to be overridden by subclasses.

### `HTMLNode.props_to_html(self) -> str`
Converts the `props` dictionary into an HTML attribute string.
- Returns a string like ` key="value"`.

### `HTMLNode.__repr__(self) -> str`
Returns a string representation of the HTMLNode object.

---

## `src/leafnode.py`

### `LeafNode.__init__(self, tag, value, props=None) -> None`
Initializes a LeafNode object, a subclass of HTMLNode for single HTML elements with a value but no children.
- `tag`: The HTML tag name.
- `value`: The content of the HTML tag. Cannot be `None`.
- `props`: Optional dictionary of HTML attributes.

### `LeafNode.__repr__(self) -> str`
Returns a string representation of the LeafNode object.

### `LeafNode.to_html(self) -> str`
Converts the LeafNode to its HTML string representation.
- Raises `ValueError` if `value` is `None`.
- If `tag` is `None`, returns just the `value`.
- Returns the HTML string (e.g., `<b>Hello</b>`).

---

## `src/parentnode.py`

### `ParentNode.__init__(self, tag, children:list, props=None) -> None`
Initializes a ParentNode object, a subclass of HTMLNode for HTML elements that can contain other HTML elements.
- `tag`: The HTML tag name. Cannot be `None`.
- `children`: A list of HTMLNode objects that are children of this node. Cannot be `None`.
- `props`: Optional dictionary of HTML attributes.

### `ParentNode.to_html(self)`
Converts the ParentNode and its children into an HTML string.
- Raises `ValueError` if `tag` or `children` is `None`.
- Returns the HTML string (e.g., `<div><p>Child</p></div>`).

---

## `src/html_parse.py`

### `text_node_to_leaf(node: TextNode) -> LeafNode`
Converts a `TextNode` object into a `LeafNode` object based on its `text_type`.
- `node`: The `TextNode` to convert.
- Returns a `LeafNode`.
- Raises `ValueError` if `TextType` is LINK or IMAGE but `url` is missing, or if `TextType` is invalid.

### `markdown_to_html_node(markdown: str) -> HTMLNode`
Converts a markdown string into a hierarchical `HTMLNode` structure.
- `markdown`: The input markdown string.
- Returns a `ParentNode` (a `div`) containing the HTML representation of the markdown.

### `text_to_children(block: str, block_type: BlockType) -> ParentNode`
Converts a markdown block and its type into a `ParentNode`.
- `block`: The markdown block string.
- `block_type`: The type of the markdown block.
- Returns a `ParentNode` representing the HTML for the block.

### `text_nodes_to_leaf_nodes(nodes: list[TextNode]) -> list[LeafNode]`
Converts a list of `TextNode` objects into a list of `LeafNode` objects.
- `nodes`: A list of `TextNode` objects.
- Returns a list of `LeafNode` objects.

### `heading_count(block: str)`
Counts the number of '#' characters at the beginning of a heading markdown block.
- `block`: A heading markdown block string.
- Returns an integer representing the heading level.

### `list_to_html(block: str, block_type: BlockType) -> list[HTMLNode]`
Converts a markdown list block (ordered or unordered) into a list of `HTMLNode` (specifically `ParentNode` with 'li' tags).
- `block`: The markdown list block string.
- `block_type`: The type of the list block (`BlockType.U_LIST` or `BlockType.O_LIST`).
- Returns a list of `ParentNode` objects, each representing a list item.

---

## `src/blocks.py`

### `markdown_to_block(markdown: str) -> list[str]`
Splits a markdown string into a list of markdown block strings. Blocks are separated by double newlines.
- `markdown`: The input markdown string.
- Returns a list of strings, where each string is a markdown block.

### `block_to_block_type(block: str) -> BlockType`
Determines the `BlockType` of a given markdown block.
- `block`: A markdown block string.
- Returns the corresponding `BlockType` (e.g., `BlockType.HEADING`, `BlockType.CODE`, `BlockType.PARAGRAPH`).

---

## `src/extractors.py`

### `extract_markdown_images(text: str) -> list[tuple[str, str]]`
Extracts markdown image syntax from a given text.
- `text`: The input text.
- Returns a list of tuples, where each tuple contains (alt_text, URL).

### `extract_markdown_links(text: str) -> list[tuple[str, str]]`
Extracts markdown link syntax from a given text.
- `text`: The input text.
- Returns a list of tuples, where each tuple contains (link_text, URL).

### `extract_markdown_heading(text: str) -> tuple[str, str]`
Extracts the heading and its content from a markdown heading block.
- `text`: The input heading markdown string.
- Returns a tuple containing (heading_marker, heading_content).

### `extract_markdown_ordered_list(text: str) -> list[str]`
Extracts the numbering for each item in a markdown ordered list.
- `text`: The input ordered list markdown string.
- Returns a list of strings, where each string is the numbering (e.g., "1.", "2.").

---

## `src/inlines.py`

### `split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]`
Splits a list of `TextNode` objects by a given delimiter and assigns a new `TextType` to the delimited text.
- `old_nodes`: A list of `TextNode` objects to split.
- `delimiter`: The string delimiter to split by (e.g., "**", "`", "*").
- `text_type`: The `TextType` to assign to the text found between the delimiters.
- Returns a new list of `TextNode` objects with the splits applied.
- Raises `ValueError` if an invalid markdown syntax is found (e.g., unclosed delimiters).

### `split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]`
Splits a list of `TextNode` objects based on markdown image syntax.
- `old_nodes`: A list of `TextNode` objects.
- Returns a new list of `TextNode` objects, with image nodes correctly identified.

### `split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]`
Splits a list of `TextNode` objects based on markdown link syntax.
- `old_nodes`: A list of `TextNode` objects.
- Returns a new list of `TextNode` objects, with link nodes correctly identified.

### `text_to_TextNode(text: str) -> list[TextNode]`
Converts a raw text string containing markdown inline elements into a list of `TextNode` objects.
- `text`: The input text string.
- Returns a list of `TextNode` objects.

---

## `src/sitegen.py`

### `copy_static(source: str, destination: str, dest_clear: bool = False)`
Recursively copies files and directories from a source path to a destination path.
If `dest_clear` is `False` and the destination exists, it will be cleared before copying.
- `source`: The source directory path.
- `destination`: The destination directory path.
- `dest_clear`: A boolean indicating whether to clear the destination directory before copying. Defaults to `False`.
- Raises `OSError` if the source path does not exist.

---

## `src/main.py`

### `main() -> None`
The main function to run the static site generator.
It prints a message and calls `copy_static` to copy files from `STATIC_PATH` to `PUBLIC_PATH`.
