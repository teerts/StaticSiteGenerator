import unittest 
from helpers import text_node_to_html_node
from textnode import TextNode, TextType

class TestHelpers(unittest.TestCase): 
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
