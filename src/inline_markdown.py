from textnode import TextNode, TextType

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_nodes = node.text.split(delimiter)

            if len(split_nodes) % 2 == 0:
                raise Exception("Invalid markdown syntax")

            type = TextType.TEXT

            for s_node in split_nodes:
                new_nodes.append(TextNode(s_node, type,))

                if type == TextType.TEXT:
                    type = text_type
                else:
                    type = TextType.TEXT
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        found_images = extract_markdown_images(original_text)

        if not found_images:
            new_nodes.append(old_node)
            continue

        for image in found_images:
            alt_text, image_url = image[0], image[1]

            split_node = original_text.split(f"![{alt_text}]({image_url})", 1)

            if len(split_node) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

            original_text = split_node[1]

        if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        found_links = extract_markdown_links(original_text)

        if not found_links:
            new_nodes.append(old_node)
            continue

        for link in found_links:
            alt_text, link_url = link[0], link[1]

            split_node = original_text.split(f"[{alt_text}]({link_url})", 1)

            if len(split_node) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, link_url))

            original_text = split_node[1]

        if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes

