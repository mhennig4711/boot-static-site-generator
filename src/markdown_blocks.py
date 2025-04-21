from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HtmlNode, LeafNode, ParentNode
import parsing_inline

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def markdown_to_blocks(markdown: str) -> list[str]:
    result = []
    for s in markdown.split("\n\n"):
        s = s.strip()
        if s != '':
            result.append(s)
    return result

def block_to_blocktype(block: str) -> BlockType:
    if block.startswith("#") and not block.startswith("#######"):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()

    if all_strings_start_with(lines, ">"):
        return BlockType.QUOTE

    if all_strings_start_with(lines, "- "):
        return BlockType.UNORDERED_LIST

    if block_is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def all_strings_start_with(strings: list[str], start: str) -> bool:
    for s in strings:
        if not s.startswith(start):
            return False
    return True

def block_is_ordered_list(lines: list[str]) -> bool:
    for i, line in enumerate(lines):
        start = f"{i+1}. "
        if not line.startswith(start):
            return False
    return True

def markdown_to_html_node(markdown: str) -> HtmlNode:
    children = []

    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:

        bt = block_to_blocktype(block)
        match (bt):

            case BlockType.PARAGRAPH:
                child_nodes = text_to_html_children(block)
                node = ParentNode("p", child_nodes)
                children.append(node)

            case BlockType.HEADING:
                text, header_level = strip_leading_chars(block, "#")
                child_nodes = text_to_html_children(text)
                node = ParentNode(f"h{header_level}", child_nodes)
                children.append(node)

            case BlockType.UNORDERED_LIST:
                child_nodes = text_to_html_list_nodes(block)
                node = ParentNode("ul", child_nodes)
                children.append(node)

            case BlockType.ORDERED_LIST:
                child_nodes = text_to_html_list_nodes(block)
                node = ParentNode("ol", child_nodes)
                children.append(node)

            case BlockType.QUOTE:
                text = "\n".join(map(lambda x: x[x.find(" "):].strip(), block.splitlines()))
                html_nodes = text_to_html_children(text)
                node = ParentNode("blockquote", html_nodes)
                children.append(node)

            case BlockType.CODE:
                text = block.strip("```")
                child_node = LeafNode("code", text)
                node = ParentNode("pre", [child_node])
                children.append(node)

            case _:
                raise Exception(f"unhandled BlockType: '{bt}'")

    return ParentNode("div", children)


def text_to_html_children(text: str) -> list[HtmlNode]:
    text_nodes = parsing_inline.text_to_text_nodes(text)
    child_nodes = list(map(text_node_to_html_node, text_nodes))
    return child_nodes

def text_to_html_list_nodes(text: str) -> list[HtmlNode]:
    child_nodes = []
    for line in text.splitlines():
        line = line[line.find(" "):].strip()
        text_nodes = parsing_inline.text_to_text_nodes(line)
        html_nodes = list(map(text_node_to_html_node, text_nodes))
        child_nodes.append(ParentNode("li", html_nodes))
    return child_nodes

def strip_leading_chars(text: str, char: str) -> (str, int):
    for i in range(len(text)):
        if text[i] != char:
            return text[i:].strip(), i
    return text, 0
