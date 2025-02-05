from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    """
    It's an intermediate representation between Markdown and HTML,
    and is specific to inline markup.
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        # Are both the same object?
        if not isinstance(value, TextNode):
            return False
        
        # Compare all three properties
        return (
            self.text == value.text and
            self.text_type == value.text_type and
            self.url == value.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"