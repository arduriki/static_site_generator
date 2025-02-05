import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
