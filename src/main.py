from textnode import TextNode
from textnode import TextType

def main() -> None:
    node = TextNode("This is some text", TextType.PLAIN_TEXT, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
