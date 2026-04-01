from leafnode import LeafNode
from textnode import TextNode, TextType

def main() -> None:
    node = TextNode("This is some text", TextType.PLAIN_TEXT, "https://www.boot.dev")
    print(node)

def text_node_to_leaf(node: TextNode) -> LeafNode:
        match node.text_type:
            case TextType.PLAIN_TEXT:
                return LeafNode(None, node.text)
            case TextType.BOLD:
                return LeafNode("b", node.text)
            case TextType.ITALIC:
                return LeafNode("i", node.text)
            case TextType.CODE:
                return LeafNode("code", node.text)
            case TextType.LINK:
                return LeafNode("a", node.text, {"href":node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":node.url, "alt":node.text})
            case _:
                raise ValueError(f"{node}, does not have valid TextType {node.text_type}")

if __name__ == "__main__":
    main()
