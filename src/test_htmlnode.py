import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode() 
        self.assertEqual(node, node2) 

    def test_neq(self): 
        node = HTMLNode() 
        node2 = HTMLNode("p") 
        self.assertNotEqual(node, node2) 

    def test_props_to_html(self): 
        props = {"href": "https://www.google.com", "target": "_blank",}
        expected_props_to_html_conversion = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(None,None,None,props)
        observed_props_to_html_conversion = node.props_to_html() 
        self.assertEqual(expected_props_to_html_conversion, observed_props_to_html_conversion)          




