from htmlnode import ParentNode
from textnode import TextNode, TextType
from text_processing import text_to_children, text_node_to_html_node

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