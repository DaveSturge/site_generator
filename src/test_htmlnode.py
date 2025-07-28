import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "This is a paragraph", [], {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph", [], {"href": "https://www.google.com"})
        self.assertEqual(' href="https://www.google.com"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph", None, {"href": "https://www.google.com"})
        self.assertEqual("HTMLNode: p, This is a paragraph, None, {'href': 'https://www.google.com'}", repr(node))

    def test_values(self):
        node = HTMLNode("div","I wish I could read",)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props,None)

if __name__ == "__main__":
    unittest.main()