from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] 
    for node in old_nodes:
        if node.text == "":
            return None

        # Not a text type node 
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)
            continue 

        split_parts = node.text.split(delimiter) 

        # No delimiter found based on split
        if len(split_parts) == 1:
            new_nodes.append(node)
            continue 

        # Unmatched delimiter 
        if len(split_parts) % 2 == 0:
            raise ValueError("Unmatched delimiter")        

        for i in range(len(split_parts)):
            split_part = split_parts[i] 
            if split_part == "":
                continue 
            if i % 2 == 0: 
                new_nodes.append(TextNode(split_part, TextType.TEXT))
            else: 
                new_nodes.append(TextNode(split_part, text_type))            
    return new_nodes

def extract_markdown_images(text):
    # Regex pattern to match markdown image syntax: ![alt text](url)
    # regexr.com for interactive regex testing. 
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"    
    
    matches = re.findall(pattern, text)
    
    return matches

def extract_markdown_links(text):    
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"   
    
    matches = re.findall(pattern, text)
    
    return matches
