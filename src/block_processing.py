import re
from constants import BlockType

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