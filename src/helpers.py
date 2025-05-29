from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text) 
    elif text_node.text_type == TextType.CODE_TEXT: 
        return LeafNode("code", text_node.text) 
    elif text_node.text_type == TextType.LINK_TEXT:
        if not hasattr(text_node, "url") or text_node.url is None:
            raise ValueError("LINK TextNode must have a 'url' attribute.") 
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE_TEXT:
        if not hasattr(text_node, "url") or text_node.url is None:
            raise ValueError("IMMAGE TextNode must have 'url' attribute.") 
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) 
    else: 
        raise ValueError(f"Unknown TextType: {text_node.text_type}")


