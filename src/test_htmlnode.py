import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_text_node(self):
        node = HTMLNode(value="Hello, world!")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_link_node(self):
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertIsNone(node.children)
        self.assertEqual(
            node.props, {"href": "https://www.boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.boot.dev" target="_blank"'
        )

    def test_parent_node(self):
        text_node = HTMLNode(value="Hello, world!")
        link_node = HTMLNode(
            tag="a", value="Click me", props={"href": "https://www.boot.dev"}
        )
        parent_node = HTMLNode(tag="div", children=[text_node, link_node])
        self.assertEqual(parent_node.tag, "div")
        self.assertIsNone(parent_node.value)
        self.assertEqual(len(parent_node.children), 2)
        self.assertIsNone(parent_node.props)
        self.assertEqual(parent_node.children[0].value, "Hello, world!")
        self.assertEqual(parent_node.children[1].tag, "a")


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_node_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_node_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
