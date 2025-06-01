import unittest 
from helpers import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from textnode import TextNode, TextType
from constants import BlockType

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
        self.assertEqual(result, [])

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

    def test_text_to_textnodes_boldtext(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [TextNode("This is ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD_TEXT),
                    TextNode(" text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_image(self):
        text = "Here is an ![alt](http://img.com) image."
        result = text_to_textnodes(text)
        expected = [TextNode("Here is an ", TextType.TEXT),
                    TextNode("alt", TextType.IMAGE_TEXT, "http://img.com"),
                    TextNode(" image.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_link(self):
        text = "Go to [site](https://example.com) now."
        result = text_to_textnodes(text)
        expected = [TextNode("Go to ", TextType.TEXT),
                    TextNode("site", TextType.LINK_TEXT, "https://example.com"),
                    TextNode(" now.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_multiple_images_and_links(self):
        text = "![a](a.png) and [b](b.com) and ![c](c.png)"
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT),
                    TextNode("a", TextType.IMAGE_TEXT, "a.png"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("b", TextType.LINK_TEXT, "b.com"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("c", TextType.IMAGE_TEXT, "c.png")]
        
        expected = [n for n in expected if not (n.text == "" and n.text_type == TextType.TEXT)]
        result = [n for n in result if not (n.text == "" and n.text_type == TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://google.com)"
        result = text_to_textnodes(text)
        expected = [TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD_TEXT),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC_TEXT),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE_TEXT),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK_TEXT, "https://google.com"),]
        
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        """Test with a single block (no double newlines)"""
        md = "This is just one paragraph with no breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just one paragraph with no breaks."])

    def test_markdown_to_blocks_excessive_newlines(self):
        """Test with excessive newlines between blocks"""
        md = """First paragraph


Second paragraph



Third paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_markdown_to_blocks_whitespace_handling(self):
        """Test that leading/trailing whitespace is stripped from blocks"""
        md = """   First paragraph with leading spaces   

Second paragraph also has spaces  

    Third paragraph too    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph with leading spaces",
                "Second paragraph also has spaces",
                "Third paragraph too",
            ],
        )

    def test_markdown_to_blocks_only_newlines(self):
        """Test with string containing only newlines"""
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_heading_single_hash(self):
        """Test heading with single #"""
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        """Test headings with 2-6 # characters"""
        test_cases = [
            "## Level 2 heading",
            "### Level 3 heading", 
            "#### Level 4 heading",
            "##### Level 5 heading",
            "###### Level 6 heading"
        ]
        for block in test_cases:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_invalid_no_space(self):
        """Test that # without space is not a heading"""
        block = "#Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_invalid_too_many_hashes(self):
        """Test that more than 6 # characters is not a heading"""
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block_simple(self):
        """Test simple code block"""
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
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
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
    


    

