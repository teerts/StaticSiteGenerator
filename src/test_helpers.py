import unittest 
from helpers import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to website](https://www.test.com) and [to youtube](https://www.youtube.com/@test)")
        self.assertListEqual([("to website", "https://www.test.com"), ("to youtube", "https://www.youtube.com/@test")], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode("Go to [test](https://test.com) now.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Go to ", TextType.TEXT),
                    TextNode("test", TextType.LINK_TEXT, "https://test.com"),
                    TextNode(" now.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("Visit [A](http://a.com) and [B](http://b.com) together.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Visit ", TextType.TEXT),
                    TextNode("A", TextType.LINK_TEXT, "http://a.com"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("B", TextType.LINK_TEXT, "http://b.com"),
                    TextNode(" together.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[Start](http://start.com) of sentence.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Start", TextType.LINK_TEXT, "http://start.com"),
                    TextNode(" of sentence.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("End with [link](http://end.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("End with ", TextType.TEXT),
                    TextNode("link", TextType.LINK_TEXT, "http://end.com")]
        self.assertEqual(result, expected)

    def test_consecutive_links(self):
        node = TextNode("[A](http://a.com)[B](http://b.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("A", TextType.LINK_TEXT, "http://a.com"),
                    TextNode("B", TextType.LINK_TEXT, "http://b.com")]
        self.assertEqual(result, expected)

    def test_only_link(self):
        node = TextNode("[Only](http://only.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("Only", TextType.LINK_TEXT, "http://only.com")]
        self.assertEqual(result, expected)

    def test_non_text_type_node(self):
        node = TextNode("Bold text", TextType.BOLD_TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_no_empty_nodes(self):
        node = TextNode("[A](http://a.com)", TextType.TEXT)
        result = split_nodes_link([node])        
        for n in result:
            self.assertTrue(n.text != "")

    


    

