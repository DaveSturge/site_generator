from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    result = []

    for block in blocks:

        if block == "":
            continue
        
        block = block.strip()

        result.append(block)

    return result

def block_to_block_type(markdown_block):

    lines = markdown_block.splitlines()

    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1:
        if lines[0].startswith("```") and lines[-1].endswith("```"):
            return BlockType.CODE
    else:
        if markdown_block.startswith("```") and markdown_block.endswith("```"):
            return BlockType.CODE
    
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            
        return BlockType.QUOTE
    
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            
        return BlockType.UNORDERED_LIST
    
    if markdown_block.startswith("1. "):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
            
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH