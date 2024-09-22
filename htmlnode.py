import re

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


class TextNode(LeafNode):
	def __init__(self, content, text_type):
		super().__init__(tag=None, value=content, children=None, props=None)
		self.content = content
		self.text_type = text_type



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


def extract_markdown_images(text):
	pattern = r"!\[(.*?)\]\((.*?)\)"
	matches = re.findall(pattern, text)
	return matches

def extract_markdown_links(text):
        pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
        matches = re.findall(pattern, text)
        return matches


def split_nodes_image(old_nodes):
        new_nodes = []
        for node in old_nodes:
                images = extract_markdown_images(node.content)
		if images:
			content = node.content
			for alt_text, image_url in images:
				markdown_pattern = f"![{alt_text}]({image_url})"
			
				sections = content.split(markdown_pattern, 1)

				if sections[0]:
					new_nodes.append(TextNode(sections[0], "text" ))

				content = sections[1] if len(sections) > 1 else ""
			
			if content:
				new_nodes.append(TextNode(content, "text"))

		else:
			new_nodes.append(node)

	return new_nodes


def split_nodes_links(old_nodes):
        new_nodes = []
        for node in old_nodes:
                links = extract_markdown_links(node.content)
                if links:
                        content = node.content
                        for link_text, url in links:
                                markdown_pattern = f"[{link_text}]({url})"

                                sections = content.split(markdown_pattern, 1)

                                if sections[0]:
                                        new_nodes.append(TextNode(sections[0], "text"))
				
				new_nodes.append(TextNode(link_text, "link", url))
                                content = sections[1] if len(sections) > 1 else ""
				
                        if content:
                                new_nodes.append(TextNode(content, "text"))

                else:
                        new_nodes.append(node)

        return new_nodes

