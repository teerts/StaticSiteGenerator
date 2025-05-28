import unittest

from htmlnode import HTMLNode, LeafNode

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
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")   

    def test_leaf_node_eq(self):    
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!") 
        self.assertEqual(node.to_html(), node2.to_html())

    def test_leaf_node_neq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world")
        self.assertNotEqual(node, node2) 

    def test_leaf_to_html_f(self):
        node = LeafNode("p", "Hello, world!") 
        self.assertNotEqual(node.to_html(), "Wayne's World!") 

    def test_value_none_yields_exception(self): 
        with self.assertRaises(ValueError) as context:
            LeafNode("p", None)
        self.assertEqual(str(context.exception), "LeafNode must have a value.") 





