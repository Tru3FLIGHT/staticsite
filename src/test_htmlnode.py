import unittest

from htmlnode import HTMLNode

class testhtmlnode(unittest.TestCase):
    dic =  {"href": "https://www.google.com", "taget": "_blank",}
    node = HTMLNode("bob", "ted", ["bill", "FaZe lacy"], dic )
    def test_repr(self):
        print(self.node)


    def test_props_wvals(self):
        print(self.node.props_to_html())

    def test_props_nvals(self):
        node = HTMLNode("bob", "ted", ["bill", "FaZe lacy"])
        print(f"response ={node.props_to_html()}")
