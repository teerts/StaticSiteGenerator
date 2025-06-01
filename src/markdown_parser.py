from htmlnode import ParentNode
from constants import BlockType
from block_processing import markdown_to_blocks, block_to_block_type
from block_converters import (
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    paragraph_to_html_node
)

def block_to_html_node(block, block_type):
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:  
        return paragraph_to_html_node(block)

def markdown_to_html_node(markdown):    
    blocks = markdown_to_blocks(markdown)    

    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        block_nodes.append(html_node)
    
    return ParentNode("div", block_nodes)