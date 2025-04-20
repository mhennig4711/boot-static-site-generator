import unittest

from textnode import TextNode, TextType
from parsing_inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes

class SplitTextNodeTest(unittest.TestCase):

    def test_no_closing_tag(self):
        with self.assertRaises(Exception):
            node = TextNode("**bold text** normal text **bold without closing tag", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_none(self):
        node = TextNode("This is text with no styling.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with no styling.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_begin(self):
        node = TextNode("**bold text** normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold text", TextType.BOLD),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_middle(self):
        node = TextNode("normal text **bold text** normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_end(self):
        node = TextNode("normal text **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_with_italic(self):
        node = TextNode("normal text **bold text** _italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" _italic text_", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_and_italic(self):
        node = TextNode("normal text **bold text** and normal text _and italic text_ and more normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and normal text ", TextType.TEXT),
            TextNode("and italic text", TextType.ITALIC),
            TextNode(" and more normal text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractImages(unittest.TestCase):

    def test_none(self):
        actual = extract_markdown_images("this is just normal text")
        expected = []
        self.assertEqual(actual, expected)

    def test_one_image(self):
        actual = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(actual, expected)

    def test_two_images(self):
        actual = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(actual, expected)

    def test_link(self):
        actual = extract_markdown_images("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected = []
        self.assertEqual(actual, expected)


class TestExtractLinks(unittest.TestCase):

    def test_none(self):
        actual = extract_markdown_links("this is just normal text")
        expected = []
        self.assertEqual(actual, expected)

    def test_one_image(self):
        actual = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(actual, expected)

    def test_two_images(self):
        actual = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(actual, expected)

    def test_white_space(self):
        actual = extract_markdown_links("This is text with a [  rick roll  ](  https://i.imgur.com/aKaOqIh.gif  )")
        expected = [("  rick roll  ", "  https://i.imgur.com/aKaOqIh.gif  ")]
        self.assertEqual(actual, expected)

    def test_image(self):
        actual = extract_markdown_links("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        expected = []
        self.assertEqual(actual, expected)


class TestSplitImages(unittest.TestCase):

    def test_no_image(self):
        node = TextNode("just some normal text", TextType.TEXT)
        actual = split_nodes_image([node])
        expected = [TextNode("just some normal text", TextType.TEXT)]
        self.assertEqual(expected, actual)

    def test_one_image_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and some text for you", TextType.TEXT)
        actual = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some text for you", TextType.TEXT),
        ]
        self.assertEqual(expected, actual)

    def test_one_image_middle(self):
        node = TextNode("Check this out: ![image](https://i.imgur.com/zjjcJKZ.png) and some text for you", TextType.TEXT)
        actual = split_nodes_image([node])
        expected = [
            TextNode("Check this out: ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some text for you", TextType.TEXT),
        ]
        self.assertEqual(expected, actual)

    def test_one_image_end(self):
        node = TextNode("Check this out: ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        actual = split_nodes_image([node])
        expected = [
            TextNode("Check this out: ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(expected, actual)

    def test_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        actual = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            actual,
        )


class TestSplitLink(unittest.TestCase):

    def test_no_link(self):
        node = TextNode("just some normal text", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [TextNode("just some normal text", TextType.TEXT)]
        self.assertEqual(expected, actual)

    def test_one_link_start(self):
        node = TextNode("[image](https://i.imgur.com/zjjcJKZ.png) and some text for you", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some text for you", TextType.TEXT),
        ]
        self.assertEqual(expected, actual)

    def test_one_link_middle(self):
        node = TextNode("Check this out: [image](https://i.imgur.com/zjjcJKZ.png) and some text for you", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [
            TextNode("Check this out: ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and some text for you", TextType.TEXT),
        ]
        self.assertEqual(expected, actual)

    def test_one_link_end(self):
        node = TextNode("Check this out: [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [
            TextNode("Check this out: ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(expected, actual)

    def test_two_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        actual = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            actual,
        )


class TestParseText(unittest.TestCase):

    def test_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
