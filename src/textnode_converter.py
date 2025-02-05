from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    """Convert a TextNode to its corresponding HTMLNode representation"""
    if not isinstance(text_node, TextNode):
        raise ValueError("Expected a TextNode")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        # Handle self-closing img tag
        if text_node.url is None:
            raise ValueError("Image nodes must have a URL")
        return f'<img src="{text_node.url}" alt="{text_node.text}">'
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")
