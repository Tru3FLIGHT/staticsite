import unittest

from enums import BlockType
from htmlnode import HTMLNode
from html_parse import text_to_children
from leafnode import LeafNode
from parentnode import ParentNode

class testhtmlnode(unittest.TestCase):
    dic =  {"href": "https://www.google.com", "taget": "_blank",}
    node = HTMLNode("bob", "ted", ["bill", "FaZe lacy"], dic )
    def test_repr(self):
        #print(self.node)
        pass


    def test_props_wvals(self):
        pass

    def test_props_nvals(self):
        node = HTMLNode("bob", "ted", ["bill", "FaZe lacy"])
        #print(f"response ={node.props_to_html()}")

#     def test_text_to_children_ol(self):
#         block = """1. Hello
# 2. This is an ordered list
# 3. we are **testing** this mf
# 4. work
# """
#         exp_out = ParentNode("ol",[
#             ParentNode("li", [
#                 LeafNode(None, "Hello")
#             ]),
#             ParentNode("li", [
#                 LeafNode(None, "This is an ordered list")
#             ]),
#             ParentNode("li", [
#                 LeafNode(None, "we are "),
#                 LeafNode("b", "testing"),
#                 LeafNode(None, " this mf")
#             ]),
#             ParentNode("li", [
#                 LeafNode(None, "work")
#             ]),
#         ])
#         print("\n" + exp_out.to_html())
#         print(text_to_children(block, BlockType.O_LIST).to_html())
#         self.assertEqual(text_to_children(block, BlockType.O_LIST),exp_out)
