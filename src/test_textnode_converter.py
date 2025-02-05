import unittest
from textnode import TextNode, TextType
from textnode_converter import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_text(self):
        node = TextNode("Just text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Just text")

    def test_text_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>Code text</code>")

    def test_text_node_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.google.com">Click me</a>'
        )

    def test_text_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html = text_node_to_html_node(node)
        self.assertEqual(
            html, '<img src="https://example.com/image.png" alt="Alt text">'
        )

    def test_text_node_invalid_type(self):
        # Create an invalid TextType for testing
        node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node("Not a TextNode")


if __name__ == "__main__":
    unittest.main()
