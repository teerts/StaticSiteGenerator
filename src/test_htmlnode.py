import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_multiple_grandchildren(self): 
        child_one = LeafNode("span", "one") 
        child_two = LeafNode("span", "two") 
        parent = ParentNode("div", [child_one, child_two]) 
        self.assertEqual(parent.to_html(), "<div><span>one</span><span>two</span></div>") 

    def test_to_html_grandchild_nested_child(self): 
        grandchild_one = LeafNode("b", "g1") 
        grandchild_two = LeafNode("b", "g2") 
        child_one = ParentNode("span", [grandchild_one]) 
        child_two = ParentNode("span", [grandchild_two]) 
        parent = ParentNode("div", [child_one, child_two]) 
        self.assertEqual(parent.to_html(), "<div><span><b>g1</b></span><span><b>g2</b></span></div>") 

    def test_raise_no_tag_valueexception(self):
        child = LeafNode("span", "child") 
        with self.assertRaises(ValueError) as context: 
            ParentNode(None, [child])  
        self.assertEqual(str(context.exception), "ParentNode must have a tag.") 

    def test_raise_no_children_valueexception(self): 
        with self.assertRaises(ValueError) as context: 
            ParentNode("div", None) 
        self.assertEqual(str(context.exception), "ParentNode must have children.") 
