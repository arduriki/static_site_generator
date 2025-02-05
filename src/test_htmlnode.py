import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(
            tag="a",
            value="Click me!",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        # Node without props should handle it gracefully
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props(self):
        # Node with empty props dictionary
        node = HTMLNode(tag="div", children=[], props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        # Node with single prop
        node = HTMLNode(tag="p", value="Styled text", props={"class": "text-bold"})
        self.assertEqual(node.props_to_html(), 'class="text-bold"')

    def test_props_to_html_no_tag(self):
        # Raw text node with props should still handle props correctly
        node = HTMLNode(value="Raw text", props={"class": "text-italic"})
        self.assertEqual(node.props_to_html(), 'class="text-italic"')

    def test_props_to_html_with_children(self):
        # Node with children and props
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(tag="div", children=[child], props={"class": "parent"})
        self.assertEqual(node.props_to_html(), 'class="parent"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text</p>")

    def test_leaf_node_with_tag_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_node_with_empty_props(self):
        node = LeafNode("p", "Text with empty props", {})
        self.assertEqual(node.to_html(), "<p>Text with empty props</p>")

    def test_leaf_node_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_node_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com", "target": "_blank", "class": "link"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank" class="link">Click me!</a>',
        )


if __name__ == "__main__":
    unittest.main()
