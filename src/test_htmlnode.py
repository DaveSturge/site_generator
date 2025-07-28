import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_props(self):
        node = LeafNode("a", "Click me!", None)
        self.assertEqual(node.to_html(), '<a>Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

    def test_to_html_many_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",)

    def test_to_html_parent_with_props_and_children(self):
        node = ParentNode("a", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")], {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com"><b>Bold text</b>Normal text</a>')

    def test_children_with_props(self):
        node = ParentNode("p", [LeafNode("a", "Click here", {"href": "https://www.google.com"}), LeafNode("i", "italic text")])
        self.assertEqual(node.to_html(), '<p><a href="https://www.google.com">Click here</a><i>italic text</i></p>')

    def test_parent_missing_tag(self):
        node = ParentNode(None, [LeafNode("i", "italic text")])
        with self.assertRaises(ValueError):
            node.to_html()



if __name__ == "__main__":
    unittest.main()