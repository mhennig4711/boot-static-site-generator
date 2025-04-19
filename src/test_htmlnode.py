import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):

    def test_convert_props_none(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), '')

    def test_convert_props_empty(self):
        node = HtmlNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_convert_props_oneProperty(self):
        node = HtmlNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_convert_props_twoProperty(self):
        node = HtmlNode(props={
            "href": "https://www.google.com"
            ,"target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_noTag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_properties(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, None).to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_to_html_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = '<div><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_nested_parents(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("span", [
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ])
            ]
        )
        expected = '<p><b>Bold text</b>Normal text<span><i>italic text</i>Normal text</span></p>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_child_props(self):
        child1 = LeafNode("span", "child")
        child2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child1, child2])
        expected = '<div>' + '<span>child</span>' + '<a href="https://www.google.com">Click me!</a>' + '</div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_props(self):
        child1 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child1], {"property1": "value1"})
        expected = '<div property1="value1">' + '<span>child</span>' + '</div>'
        self.assertEqual(parent_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
