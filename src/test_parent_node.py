import unittest
from parent_node import ParentNode
from leaf_node import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        # Test basic parent node with a single child
        node = ParentNode("div", [LeafNode("p", "Hello, World!")])
        self.assertEqual(node.to_html(), "<div><p>Hello, World!</p></div>")

    def test_parent_node_multiple_children(self):
        # Test parent node with multiple children
        node = ParentNode(
            "div", [LeafNode("p", "First paragraph"), LeafNode("p", "Second paragraph")]
        )
        self.assertEqual(
            node.to_html(), "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )

    def test_parent_node_with_props(self):
        # Test parent node with properties
        node = ParentNode(
            "div", [LeafNode("p", "Content")], {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(), '<div class="container" id="main"><p>Content</p></div>'
        )

    def test_parent_node_nested(self):
        # Test nested parent nodes
        inner_node = ParentNode(
            "div", [LeafNode("p", "Inner content")], {"class": "inner"}
        )
        outer_node = ParentNode("div", [inner_node], {"class": "outer"})
        self.assertEqual(
            outer_node.to_html(),
            '<div class="outer"><div class="inner"><p>Inner content</p></div></div>',
        )

    def test_parent_node_mixed_children(self):
        # Test parent node with mix of leaf nodes with and without tags
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_no_tag(self):
        # Test that ValueError is raised when tag is None
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("p", "Content")])
            node.to_html()
        self.assertTrue("Parent node must have a tag" in str(context.exception))

    def test_no_children(self):
        # Test that ValueError is raised when children is None
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", None)
            node.to_html()
        self.assertTrue("Parent node must have children" in str(context.exception))

    def test_empty_children_list(self):
        # Test parent node with empty children list
        node = ParentNode("div", [], {"class": "empty"})
        self.assertEqual(node.to_html(), '<div class="empty"></div>')

    def test_complex_nesting(self):
        # Test complex nesting with multiple levels and mixed content
        node = ParentNode(
            "article",
            [
                ParentNode(
                    "header", [LeafNode("h1", "Title")], {"class": "article-header"}
                ),
                ParentNode(
                    "section",
                    [
                        LeafNode("p", "First paragraph"),
                        ParentNode(
                            "div",
                            [
                                LeafNode("p", "Nested paragraph"),
                                LeafNode("p", "Another nested paragraph"),
                            ],
                            {"class": "nested"},
                        ),
                    ],
                    {"class": "content"},
                ),
            ],
            {"id": "main-article"},
        )
        expected = (
            '<article id="main-article">'
            '<header class="article-header"><h1>Title</h1></header>'
            '<section class="content"><p>First paragraph</p>'
            '<div class="nested"><p>Nested paragraph</p><p>Another nested paragraph</p></div>'
            "</section></article>"
        )
        self.assertEqual(node.to_html(), expected)
