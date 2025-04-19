
class HtmlNode:
    def __init__(self, tag: str =None, value: str =None, children: list =None, props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or len(self.props) <= 0:
            return ""
        res = ''
        for k, v in self.props.items():
            res += f' {k}="{v}"'
        return res


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict =None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("no value")
        if self.tag == None:
            return self.value

        res = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return res


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict =None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("no tag")
        if self.children == None or len(self.children) <= 0:
            raise ValueError("no children")

        res = ''
        res += f'<{self.tag}{self.props_to_html()}>'
        for ch in self.children:
            res += ch.to_html()
        res += f'</{self.tag}>'
        return res
