import unittest 

from textnode import TextNode, TextType 

class TestTextNode(unittest.TestCase):
    def test_eq(self): 
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT) 
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a bold text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a italic text node", TextType.ITALIC_TEXT) 
        self.assertNotEqual(node, node2) 

    def test_url_property_input_eq(self):
        node = TextNode("Url property works", TextType.BOLD_TEXT, "www.test.com") 
        node2 = TextNode("Url property works", TextType.BOLD_TEXT, "www.test.com") 
        self.assertEqual(node, node2) 

    def test_url_property_input_neq(self):
        node = TextNode("Node", TextType.BOLD_TEXT) 
        node2 = TextNode("Node2", TextType.BOLD_TEXT, "www.test.com") 
        self.assertNotEqual(node, node2) 

if __name__ == "__main__":
    unittest.main()
