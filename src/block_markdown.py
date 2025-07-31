from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node, TextType, TextNode
from inline_markdown import text_to_textnodes

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    block_node = None

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            block_lines = block.splitlines()

            for line in block_lines:
                line.strip()

            block_text = " ".join(block_lines)

            child_html_nodes = text_to_children(block_text)

            block_node = ParentNode("p", child_html_nodes)

        if block_type == BlockType.HEADING:
            heading_count = 0

            for i in range(0,6):
                if i >= len(block) or block[i] != "#":
                    break
                
                heading_count += 1

            block_text = block[heading_count + 1:]
            child_html_nodes = text_to_children(block_text)

            block_node = ParentNode(f"h{heading_count}", child_html_nodes)

        if block_type == BlockType.CODE:
            code_text = TextNode(block[3:-3].lstrip("\n"), TextType.TEXT)            

            child = text_node_to_html_node(code_text)
            code = ParentNode("code", [child])
            block_node = ParentNode("pre", [code])

        if block_type == BlockType.QUOTE:
            lines = block.splitlines()

            processed_lines = []

            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("Invalid quote block")
                
                processed_lines.append(line.lstrip(">").strip())

            full_quote = " ".join(processed_lines)

            child_html_nodes = text_to_children(full_quote)

            block_node = ParentNode("blockquote", child_html_nodes)

        if block_type == BlockType.ORDERED_LIST:
            lines = block.splitlines()

            process_olist_lines = []

            for line in lines:
                text = line[3:]
                child_html_nodes = text_to_children(text)
                process_olist_lines.append(ParentNode("li", child_html_nodes))

            block_node = ParentNode("ol", process_olist_lines)

        if block_type == BlockType.UNORDERED_LIST:
            lines = block.splitlines()

            process_ulist_lines = []

            for line in lines:
                text = line.lstrip("-").strip()
                child_html_nodes = text_to_children(text)
                process_ulist_lines.append(ParentNode("li", child_html_nodes))

            block_node = ParentNode("ul", process_ulist_lines)

        children.append(block_node)

    return ParentNode("div", children, None)

def text_to_children(text):
    html_nodes = []

    text_nodes = text_to_textnodes(text)

    for text_node in text_nodes:
        result = text_node_to_html_node(text_node)

        html_nodes.append(result)

    return html_nodes