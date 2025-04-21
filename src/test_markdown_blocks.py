import unittest

from markdown_blocks import BlockType, markdown_to_blocks, block_to_blocktype, markdown_to_html_node


class TestMarkdownToBlock(unittest.TestCase):

    def test_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        actual = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(actual,expected)


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_blocktype("# this is a heading"))
        self.assertEqual(BlockType.HEADING, block_to_blocktype("## this is a heading"))
        self.assertEqual(BlockType.HEADING, block_to_blocktype("### this is a heading"))
        self.assertEqual(BlockType.HEADING, block_to_blocktype("#### this is a heading"))
        self.assertEqual(BlockType.HEADING, block_to_blocktype("##### this is a heading"))
        self.assertEqual(BlockType.HEADING, block_to_blocktype("###### this is a heading"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype("####### this is NOT a heading"))

    def test_code(self):
        self.assertEqual(BlockType.CODE, block_to_blocktype("""```
let add = func(x,y) x+y;
```"""))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype("""```
let add = func(x,y) x+y;
"""))

    def test_inline_quote(self):
        self.assertEqual(BlockType.QUOTE, block_to_blocktype("""> Was macht der Rote Knopf?
> Einfach mal gucken"""))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype("""> Was macht der Rote Knopf?
* Einfach mal gucken"""))

    def test_inline_unordered_list(self):
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype("""- item1
- item 2
- item 3"""))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype("""- item1
-- item 2
- item 3"""))

    def test_ordered_list(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype("""1. item1
2. item 2
3. item 3"""))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype("""1. item1
2. item 2
5. item 3"""))


class TestMarkdownToHtml(unittest.TestCase):

    def test_paragraphs_no_styling(self):
        md = """
This is paragraph
text in a p
tag here

This is another paragraph here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is paragraph\ntext in a p\ntag here</p><p>This is another paragraph here</p></div>",
        )

    def test_paragraphs_with_styling(self):
        md = """
This is **bold** paragraph
text in a p
tag here

This is another _paragraph_ here with some `inline code` in the middle

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b> paragraph\ntext in a p\ntag here</p><p>This is another <i>paragraph</i> here with some <code>inline code</code> in the middle</p></div>",
        )

    def test_heading(self):
        md = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>heading 1</h1><h2>heading 2</h2><h3>heading 3</h3><h4>heading 4</h4><h5>heading 5</h5><h6>heading 6</h6></div>",
        )

    def test_heading_with_styling(self):
        md = """
# **bold heading 1**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1><b>bold heading 1</b></h1></div>",
        )

    def test_unordered_list(self):
        md = """
- item 1
- item 2
- item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_unordered_list_with_styling(self):
        md = """
- **bold** item 1
- _italic_ item 2
- `inline code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item 1</li><li><i>italic</i> item 2</li><li><code>inline code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. item 1
2. item 2
3. item 3
4. item 4
5. item 5
6. item 6
7. item 7
8. item 8
9. item 9
10. item 10
11. item 11
12. item 12
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li><li>item 4</li><li>item 5</li><li>item 6</li><li>item 7</li><li>item 8</li><li>item 9</li><li>item 10</li><li>item 11</li><li>item 12</li></ol></div>",
        )

    def test_ordered_list_with_styling(self):
        md = """
1. **bold** item 1
2. _italic_ item 2
3. `inline code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>bold</b> item 1</li><li><i>italic</i> item 2</li><li><code>inline code</code></li></ol></div>",
        )

    def test_quotes(self):
        md = """
> Quoth the Raven
> Nevermore
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quoth the Raven\nNevermore</blockquote></div>",
        )

    def test_links(self):
        md = """
[link_text](https://www.google.com)

![img_text](url/of/image.jpg)

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><a href="https://www.google.com">link_text</a></p><p><img src="url/of/image.jpg" alt="img_text"></img></p></div>',
        )

    def test_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )



if __name__ == "__main__":
    unittest.main()
