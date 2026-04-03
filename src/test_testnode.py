import unittest

from textnode import TextNode
from enums import TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text Node", TextType.BOLD)
        node2 = TextNode("This is a text Node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_tt(self):
        node = TextNode("This is a text Node", TextType.BOLD)
        node2 = TextNode("This is a text Node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_missing_url(self):
        node = TextNode("This is a text Node", TextType.BOLD, "https://url.com")
        node2 = TextNode("This is a text Node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
