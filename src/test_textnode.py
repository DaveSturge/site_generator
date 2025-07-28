import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_image_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.youtube.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.youtube.com")
        self.assertEqual("TextNode(This is a text node, bold, https://www.youtube.com)", repr(node))


if __name__ == "__main__":
    unittest.main()