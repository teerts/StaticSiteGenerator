import unittest 
from helpers import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

class TestHelpers(unittest.TestCase): 
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_basic_bold_split(self):
        node = TextNode("This is *bold* text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD_TEXT)
        expected_node_split_result = [TextNode("This is ", TextType.TEXT),
                                      TextNode("bold", TextType.BOLD_TEXT),
                                      TextNode(" text", TextType.TEXT)]
        self.assertEqual(result, expected_node_split_result)

    def test_basic_italic_split(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        expected_node_split_result = [TextNode("This is ", TextType.TEXT),
                                      TextNode("italic", TextType.ITALIC_TEXT),
                                      TextNode(" text", TextType.TEXT)]
        self.assertEqual(result, expected_node_split_result)

    def test_basic_code_split(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_node_split_result = [TextNode("This is ", TextType.TEXT),
                                      TextNode("code", TextType.CODE_TEXT),
                                      TextNode(" text", TextType.TEXT)]
        self.assertEqual(result, expected_node_split_result)
        
    def test_multiple_delimiter_code_split(self):
        node = TextNode("This is `code` text. This is `code` text.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        expected_node_split_result = [TextNode("This is ", TextType.TEXT),
                                      TextNode("code", TextType.CODE_TEXT),
                                      TextNode(" text. This is ", TextType.TEXT),
                                      TextNode("code", TextType.CODE_TEXT),
                                      TextNode(" text.", TextType.TEXT)]
        self.assertEqual(result, expected_node_split_result)
    
    def test_no_delimiter(self):
        node = TextNode("just text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD_TEXT)
        self.assertEqual(result, [node])
    
    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched `code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.BOLD_TEXT)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD_TEXT)
        self.assertEqual(result, None)

    def test_only_delimiter(self):
        node = TextNode("*Bold Move*", TextType.TEXT)        
        result = split_nodes_delimiter([node], "*", TextType.BOLD_TEXT)
        expected_node_split_result = [TextNode("Bold Move", TextType.BOLD_TEXT)]
        self.assertEqual(result, expected_node_split_result)

    def test_multiline_delimiter_unmatched(self):
        node = TextNode("*The beginning* and the end*", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.BOLD_TEXT)

    

