
class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self):
		if not self.props:
			return ""

		formatted_props = []
		for key, value in self.props.items():
			formatted_props += [f'{key}="{value}"']
		return " " + " ".join(formatted_props)

	def __repr__(self):
		attributes = []

		if self.tag is not None:
			attributes.append(f"tag='{self.tag}'")
		if self.value is not None:
			value = self.value if len(self.value) <= 20 else self.value[:20] + "..."
			attributes.append(f"value='{value}'")
		if self.children is not None:
			if len(self.children) > 2:
				children_repr = f"[{len(self.children)} items]"
			else:
				children_repr = repr(self.children)
			attributes.append(f"children={children_repr}")
		if self.props is not None:
			attributes.append(f"props='{self.props}'")
		return f"HTMLNode({', '.join(attributes)})"


class LeafNode(HTMLNode):
	def __init__(self, value, tag=None, props=None):
		super().__init__(tag=tag, value=value, children=None, props=props)

	def to_html(self):
		if self.value is None:
			raise ValueError("LeafNode must have a value")
		if self.tag is None:
			return self.value

		attrs = ""
		if self.props is not None:
			attrs = ' '.join([f'{key}="{value}"' for key, value in self.props.items()])
		return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
	def __init__(self, children, tag = None, props = None):
		super().__init__(children = children, tag=tag, props=props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag")
		if len(self.children) == 0:
			raise ValueError("ParentNode must have children")

		children_html = ''.join(child.to_html() for child in self.children)

		return f"<{self.tag}>{children_html}</{self.tag}>"




text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def text_node_to_html_node(text_node):


	if text_node.text_type == text_type_text:
		return LeafNode(text_node.text)

	if text_node.text_type == text_type_bold:
		return LeafNode(text_node.text, tag="b")

	if text_node.text_type == text_type_italic:
		return LeafNode(text_node.text, tag="i")

	if text_node.text_type == text_type_code:
		return LeafNode(text_node.text, tag="code")

	if text_node.text_type == text_type_link:
		return LeafNode(text_node.text, tag="a" , props={"href": text_node.url})

	if text_node.text_type == text_type_image:
		return LeafNode("", tag="img", props= {"src": text_node.url,"alt": text_node.text} )

	else:
		raise ValueError(f"Invalid text type: {text_node.text_type}")


import unittest
from collections import namedtuple

MockTextNode = namedtuple('MockTextNode', ['text_type', 'text', 'url'])

class TestTextNodeToHtmlNode(unittest.TestCase):
	def test_text_node(self):
		text_node = MockTextNode("text", "Hello, world!", None)
		html_node = text_node_to_html_node(text_node)
		self.assertIsInstance(html_node, LeafNode)
		self.assertEqual(html_node.value, "Hello, world!")
		self.assertIsNone(html_node.tag)



	def test_bold_node(self):
		bold_node = MockTextNode("bold", "Bold text", None)
		html_node = text_node_to_html_node(bold_node)
		self.assertIsInstance(html_node, LeafNode)
		self.assertEqual(html_node.value, "Bold text")
		self.assertEqual(html_node.tag, "b")

	def test_link_node(self):
		link_node = MockTextNode("link", "Click here", "https://example.com")
		html_node = text_node_to_html_node(link_node)
		self.assertIsInstance(html_node, LeafNode)
		self.assertEqual(html_node.value, "Click here")
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.props, {"href": "https://example.com"})

	def test_invalid_type(self):
		invalid_node = MockTextNode("invalid", "Invalid type", None)
		with self.assertRaises(Exception):
			text_node_to_html_node(invalid_node)
