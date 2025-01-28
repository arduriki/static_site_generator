import unittest

from text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode(
            "This is a text node with a url", TextType.NORMAL_TEXT, "http://boot.dev"
        )
        node2 = TextNode("This is a text node without a url", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
