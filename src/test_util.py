import unittest

import htmlnode
from markdown_util import *
from textnode import TextNode, TextType

class testUtil(unittest.TestCase):
#==============================
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
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

#=========================================================================



    def test_delimiter_single_bold(self):
        node = TextNode("this has **bold** text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD), [TextNode("this has ", TextType.TEXT),
                                                                             TextNode("bold", TextType.BOLD),
                                                                             TextNode(" text", TextType.TEXT)])

    def test_delimiter_single_italic(self):
        node = TextNode("this has _italic_ text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '_', TextType.ITALIC), [TextNode("this has ", TextType.TEXT),
                                                                             TextNode("italic", TextType.ITALIC),
                                                                             TextNode(" text", TextType.TEXT)])

    def test_delimiter_single_code(self):
        node = TextNode("this has `code` text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], '`', TextType.CODE), [TextNode("this has ", TextType.TEXT),
                                                                             TextNode("code", TextType.CODE),
                                                                             TextNode(" text", TextType.TEXT)])

    def test_delimier_unclosed_error(self):
        node = TextNode("this text has `errors", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimier_ending_statement(self):
        node = TextNode("this node ends with **bold**", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(out, [
            TextNode("this node ends with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])


    def test_delimiter_muilti(self):
        node = TextNode("statement **with** multiple **bold** lines", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                         [
                         TextNode("statement ", TextType.TEXT),
                         TextNode("with", TextType.BOLD),
                         TextNode(" multiple ", TextType.TEXT),
                         TextNode("bold", TextType.BOLD),
                         TextNode(" lines", TextType.TEXT)
                         ])

    def test_delimiter_multiline_recuse(self):
        node = TextNode("this statement contains **bold**, _italic_ and `code`", TextType.TEXT)
        bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
        all = split_nodes_delimiter(italic, "`", TextType.CODE)
        self.assertEqual(all, [
            TextNode("this statement contains ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ])



    def test_find_image(self):
        self.assertEqual(extract_markdown_image("This is text ![image1](url1) and also ![image2](url2)"),
                         [
                         ("image1", "url1"),
                         ("image2", "url2")
                         ])

    def test_find_image_none(self):
        self.assertEqual(extract_markdown_image("this text has no image"), [])

    def test_find_link(self):
        self.assertEqual(extract_markdown_link("this text has [link](url), and ![image](url)"),
                         [
                         ("link", "url")
                         ])


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], Split.IMAGE)
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )


    def test_split_link(self):
        node = TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], Split.LINK)
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )


    def test_split_mixed(self):
        node = TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and a ![Image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes([node], Split.LINK)
        new_new_nodes = split_nodes(new_nodes, Split.IMAGE)
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "Image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_new_nodes,
    )


    def test_to_textnode(self):
        out = text_to_TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(out,
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ])


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph


with a line inbetween
\n
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "with a line inbetween"
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
