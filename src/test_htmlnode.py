from re import L
import unittest

from enums import BlockType
from htmlnode import HTMLNode
from html_parse import markdown_to_html_node, text_to_children
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

    def test_text_to_children_ol(self):
        block = """1. Hello
2. This is an ordered list
3. we are **testing** this mf
4. work
"""
        exp_out = ParentNode("ol",[
            ParentNode("li", [
                LeafNode(None, "Hello")
            ]),
            ParentNode("li", [
                LeafNode(None, "This is an ordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "we are "),
                LeafNode("b", "testing"),
                LeafNode(None, " this mf")
            ]),
            ParentNode("li", [
                LeafNode(None, "work")
            ]),
        ])
        self.assertEqual(text_to_children(block, BlockType.O_LIST).to_html(),exp_out.to_html())

    def test_text_to_children_ul(self):
        block ="""- hello
- this is an unordered list
- we are **testing** this mf
- work
"""
        exp_out = ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "hello")
            ]),
            ParentNode("li", [
                LeafNode(None, "this is an unordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "we are "),
                LeafNode("b", "testing"),
                LeafNode(None, " this mf")
            ]),
            ParentNode("li", [
                LeafNode(None, "work")
            ])
        ])
        self.assertEqual(text_to_children(block, BlockType.U_LIST).to_html(), exp_out.to_html())

    def test_heading_tag(self):
        block = "### This is heading"
        exp_out = ParentNode("h3", [
            LeafNode(None, "This is heading")
        ])
        self.assertEqual(text_to_children(block, BlockType.HEADING).to_html(), exp_out.to_html())
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
