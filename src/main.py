from leafnode import LeafNode
from textnode import TextNode, TextType

def main() -> None:
    node = TextNode("This is some text", TextType.TEXT, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()
