import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):

    def test_eq_defaultUrl(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_customUrl(self):
        node1 = TextNode("This is a text node", TextType.LINK, "http://deez.nutz")
        node2 = TextNode("This is a text node", TextType.LINK, "http://deez.nutz")
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("text node 1", TextType.LINK, "http://deez.nutz")
        node2 = TextNode("text node 2", TextType.LINK, "http://deez.nutz")
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is a text node", TextType.LINK, "http://deez.nutz")
        node2 = TextNode("This is a text node", TextType.IMAGE, "http://deez.nutz")
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("This is a text node", TextType.LINK, "http://deez.nutz")
        node2 = TextNode("This is a text node", TextType.LINK, "http://hello.sailor")
        self.assertNotEqual(node1, node2)


class TestTextNodeConversion(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic text node")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("this is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "this is code")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("this is a link", TextType.LINK, "http://deez.nutz")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "this is a link")
        self.assertEqual(html_node.props, {"href": "http://deez.nutz"})

    def test_image(self):
        node = TextNode("image alt text", TextType.IMAGE, "url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "url/of/image.jpg", "alt": "image alt text"})


if __name__ == "__main__":
    unittest.main()
