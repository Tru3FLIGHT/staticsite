import unittest

from leafnode import LeafNode


class testleafnode(unittest.TestCase):

    def test_nodebasic(self):
        node = LeafNode("p", "This is a paragraph of text.")
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_nodewithprops(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node.to_html())
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(node)
