import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_parent_node_with_children(self):
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

    def test_parent_node_with_props(self):
        node = ParentNode(
            "div", [LeafNode("p", "Hello, world!")], {"class": "container"}
        )
        self.assertEqual(
            node.to_html(), '<div class="container"><p>Hello, world!</p></div>'
        )

    def test_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italic text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(), "<div><p><b>Bold text</b> and <i>italic text</i></p></div>"
        )

    def test_parent_node_without_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("p", "Hello")])
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_parent_node_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_parent_node_multiple_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Text")],
            {"class": "container", "id": "main", "data-test": "true"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main" data-test="true"><p>Text</p></div>',
        )

    def test_deeply_nested_structure(self):
        # Create a deeply nested structure: div > article > section > p > (b, i)
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "article",
                    [
                        ParentNode(
                            "section",
                            [
                                ParentNode(
                                    "p",
                                    [
                                        LeafNode("b", "Bold"),
                                        LeafNode(None, " and "),
                                        LeafNode("i", "italic"),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><article><section><p><b>Bold</b> and <i>italic</i></p></section></article></div>",
        )

    def test_multiple_nested_siblings(self):
        # Test multiple nested siblings at different levels
        node = ParentNode(
            "div",
            [
                ParentNode("section", [LeafNode("p", "First")], {"class": "first"}),
                ParentNode("section", [LeafNode("p", "Second")], {"class": "second"}),
                ParentNode("section", [ParentNode("div", [LeafNode("p", "Third")])]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><section class="first"><p>First</p></section><section class="second"><p>Second</p></section><section><div><p>Third</p></div></section></div>',
        )

    def test_mixed_leaf_and_parent_children(self):
        # Test mixing leaf nodes and parent nodes as siblings
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Start"),
                ParentNode("p", [LeafNode("b", "Bold")]),
                LeafNode(None, "Middle"),
                ParentNode("p", [LeafNode("i", "Italic")]),
                LeafNode(None, "End"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div>Start<p><b>Bold</b></p>Middle<p><i>Italic</i></p>End</div>",
        )

    def test_complex_props_nesting(self):
        # Test complex property inheritance and nesting
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "nav",
                    [
                        LeafNode("a", "Link 1", {"href": "#1", "class": "active"}),
                        LeafNode("a", "Link 2", {"href": "#2"}),
                    ],
                    {"class": "navbar"},
                ),
                ParentNode(
                    "main",
                    [
                        ParentNode(
                            "div",
                            [LeafNode("p", "Content")],
                            {"class": "content", "id": "main-content"},
                        )
                    ],
                    {"role": "main"},
                ),
            ],
            {"lang": "en", "dir": "ltr"},
        )
        self.assertEqual(
            node.to_html(),
            '<div lang="en" dir="ltr"><nav class="navbar"><a href="#1" class="active">Link 1</a><a href="#2">Link 2</a></nav><main role="main"><div class="content" id="main-content"><p>Content</p></div></main></div>',
        )

    def test_parent_node_with_empty_children_arrays(self):
        # Test nested structure with empty children arrays
        node = ParentNode(
            "div",
            [
                ParentNode("span", []),
                ParentNode(
                    "section",
                    [
                        ParentNode("p", []),
                        LeafNode(None, "Text"),
                        ParentNode("div", []),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><span></span><section><p></p>Text<div></div></section></div>",
        )

    def test_extreme_nesting_depth(self):
        # Create a very deeply nested structure to test stack handling
        current_node = LeafNode("span", "Deep")
        for _ in range(100):  # Create 100 levels of nesting
            current_node = ParentNode("div", [current_node])

        result = current_node.to_html()
        self.assertTrue(result.startswith("<div>" * 100))
        self.assertTrue(result.endswith("</div>" * 100))
        self.assertIn("<span>Deep</span>", result)


if __name__ == "__main__":
    unittest.main()
