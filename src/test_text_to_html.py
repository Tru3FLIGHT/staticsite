import unittest

import htmlnode
from main import text_node_to_leaf
from textnode import TextNode, TextType

class testTextToHtml(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, "This is a text node")

    def test_italics(self):
        node = TextNode("this is italic text", TextType.ITALIC)
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.tag, "i")
        self.assertEqual(htmlnode.value, "this is italic text")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "bold text")

    def test_code(self):
        node = TextNode("this is code", TextType.CODE)
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.tag, "code")
        self.assertEqual(htmlnode.value, "this is code")

    def test_link(self):
        node = TextNode("link", TextType.LINK, "www.google.com")
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.to_html(), "<a href=\"www.google.com\">link</a>")

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "image.jpg")
        htmlnode = text_node_to_leaf(node)
        self.assertEqual(htmlnode.props, {"src":"image.jpg", "alt":"alt text"})


