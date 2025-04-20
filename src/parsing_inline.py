import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        fields = node.text.split(delimiter)
        if len(fields) % 2 != 1:
            raise Exception(f"no matching closing delimiter '{delimiter}' in text '{node.text}'")

        has_styling = True
        for field in fields:
            has_styling = not has_styling
            tt = text_type if has_styling else TextType.TEXT
            if len(field) == 0:
                continue
            result.append(TextNode(field, tt))

    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            result.append(node)
            continue

        remaining = node.text
        for img_alt, img_link in images:
            # Figure out, what comes before and after this specific image field.
            # Add the before-part and the image data.
            src = f'![{img_alt}]({img_link})'
            split = remaining.split(src, maxsplit=1)
            if split[0] != "":
                result.append(TextNode(split[0], TextType.TEXT))
            result.append(TextNode(img_alt, TextType.IMAGE, img_link))
            remaining = split[1]

        # handle text parts after the last image
        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            result.append(node)
            continue

        remaining = node.text
        for text, url in links:
            # Figure out, what comes before and after this specific link field.
            # Add the before-part and the link data.
            src = f'[{text}]({url})'
            split = remaining.split(src, maxsplit=1)
            if split[0] != "":
                result.append(TextNode(split[0], TextType.TEXT))
            result.append(TextNode(text, TextType.LINK, url))
            remaining = split[1]

        # handle text parts after the last link
        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result


def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    result = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    result.extend(matches)
    return result

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    result = []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    result.extend(matches)
    return result

def text_to_text_nodes(text: str) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    return result
