from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
import re
from constants import BlockType

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
            raise ValueError("IMAGE TextNode must have 'url' attribute.") 
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) 
    else: 
        raise ValueError(f"Unknown TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] 
    for node in old_nodes:
        if node.text == "":
            continue

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)      
        
        if not matches: 
            new_nodes.append(node)
            continue 
        
        last_index = 0 
        for alt_text, url in matches: 
            markdown_string = f"![{alt_text}]({url})"
            start = text.find(markdown_string, last_index)
            end = start + len(markdown_string)

            before_text = text[last_index:start]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE_TEXT, url))

            last_index = end 

        after_text = text[last_index:]

        if after_text:
            new_nodes.append(TextNode(after_text, TextType.TEXT))       

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)      

        if not matches: 
            new_nodes.append(node)
            continue 
        
        last_index = 0 
        for alt_text, url in matches: 
            markdown_string = f"[{alt_text}]({url})"
            start = text.find(markdown_string, last_index)
            end = start + len(markdown_string)

            before_text = text[last_index:start]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK_TEXT, url))

            last_index = end 

        after_text = text[last_index:]

        if after_text:
            new_nodes.append(TextNode(after_text, TextType.TEXT))       

    return new_nodes

def text_to_textnodes(text):
    text = text.replace('\n', ' ')
    
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_image(nodes)   
    nodes = split_nodes_link(nodes)    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)    
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)    # Changed from "_" to "*"
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')

    blocks_result = []

    for block in blocks: 
        stripped_block = block.strip()

        if stripped_block: 
            blocks_result.append(stripped_block)

    return blocks_result

def block_to_block_type(block):    
    lines = block.split('\n')    

    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST    
    
    ordered_list_pattern = True
    for i in range(len(lines)):
        if not lines[i].startswith(f'{i + 1}. '):
            ordered_list_pattern = False
            break
    
    if ordered_list_pattern and len(lines) > 0:
        return BlockType.ORDERED_LIST    
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):    
    blocks = markdown_to_blocks(markdown)    

    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        block_nodes.append(html_node)
    
    return ParentNode("div", block_nodes)

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

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break    

    heading_text = block[level + 1:]    

    tag = f"h{level}"
    children = text_to_children(heading_text)
    
    return ParentNode(tag, children)

def code_to_html_node(block):
    lines = block.split('\n')
    
    if len(lines) >= 3:
        code_content = '\n'.join(lines[1:-1])

        if len(lines) > 2:
            code_content += '\n'
    else:
        code_content = block[3:-3]  
    text_node = TextNode(code_content, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)
    
    return ParentNode("pre", [ParentNode("code", [code_child])])

def quote_to_html_node(block):
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        item_text = line[2:] 
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    
    for i in range(len(lines)):
        line = lines[i]
        dot_index = line.find('. ')
        item_text = line[dot_index + 2:] 
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]












